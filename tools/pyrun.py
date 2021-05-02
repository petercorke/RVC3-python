import jupyter_client
import subprocess
import sys
import re
import argparse
from subprocess import Popen, PIPE
from threading  import Thread
from queue import Queue, Empty

debug = False

# handle command line arguments
parser = parser = argparse.ArgumentParser(description='Run Python script for RVC3 book.')
parser.add_argument('script', 
        default=None, nargs='?',
        help='the script to run')
parser.add_argument('--maxlines', '-m', 
        type=int, default=None,
        help='maximum number of lines to read, default %(default)s')
parser.add_argument('--linenumber', '-l', 
        default=False, action='store_const', const=True,
        help='show line numbers, default %(default)s')
parser.add_argument('--nocomments', '-c', 
        action='store_const', const=False, default=True, dest='comments',
        help='dont show comments, default %(default)s')
parser.add_argument('--timeout', '-t', 
        type=float, default=0.2,
        help='timeout on each IPython command, default %(default)s seconds')
args = parser.parse_args()


if args.script is None:
    print('no file specified')
    sys.exit(1)
else:
    filename = args.script

# initial commands pushed to IPython
startup = r"""
import numpy as np
%config InteractiveShell.ast_node_interactivity = 'last_expr_or_assign'
%precision %.3g
np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})

"""

def print_msg(m, indent=0):
    for k, i in m.items():
        if isinstance(i, dict):
            print(' ' * indent, f"{k}::")
            print_msg(i, indent+4)
        else:
            s = f"{k:10s}: {i}"
            if len(s) > 100:
                s = s[:100]
            print(' ' * indent, s)
    if indent == 0:
        print()


def run_cell(client, code):
    # now we can run code.  This is done on the shell channel

    # execution is immediate and async, returning a UUID
    msg_id = client.execute(code, silent=False)
    if debug:
        print(f"\nrunning: {code}\n  msg_id = {msg_id}\n")

    # there is one response message which tells how it went
    reply = client.get_shell_msg()
    if debug:
        print_msg(reply)

    assert reply['msg_type'] == 'execute_reply' and\
        reply['parent_header']['msg_id'] == msg_id, 'bad execute shell reply'

    status = reply['content']['status']
    if status == 'ok':

        # first message says busy
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'status' and\
            reply['parent_header']['msg_id'] == msg_id and\
            reply['content']['execution_state'] == 'busy', 'bad execute iopub reply'

        # second message is execute_input which reflects back the command
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'execute_input' and\
            reply['parent_header']['msg_id'] == msg_id, 'bad execute iopub reply'


        while True:
            reply = client.get_iopub_msg()
            if debug:
                print_msg(reply)
            
            # check it is a reply to this transaction
            assert reply['parent_header']['msg_id'] == msg_id, 'bad execute iopub reply'

            # check for last message in response sequence
            if reply['msg_type'] == 'status' and\
                    reply['content']['execution_state'] == 'idle':
                break

            if reply['msg_type'] == 'stream':
                # command had an output
                print(reply['content']['text'])
            elif reply['msg_type'] == 'execute_result':
                # command had an output
                print(reply['content']['data']['text/plain'])

                # get next message
            

    elif status == 'error':
        # print('Error: ', reply['content']['ename'])
        # print('  ', reply['content']['evalue'])

        # first message says busy
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'status' and\
            reply['parent_header']['msg_id'] == msg_id and\
            reply['content']['execution_state'] == 'busy', 'bad execute iopub reply'

        # second message is execute_input which reflects back the command
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'execute_input' and\
            reply['parent_header']['msg_id'] == msg_id, 'bad execute iopub reply'

        # third message is command display value
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'error' and\
            reply['parent_header']['msg_id'] == msg_id, 'bad execute iopub reply'
        print('Traceback:')
        for line in reply['content']['traceback']:
            print(line)

        # fourth message is execute_input which reflects back the command
        reply = client.get_iopub_msg()
        if debug:
            print_msg(reply)
        assert reply['msg_type'] == 'status' and\
            reply['parent_header']['msg_id'] == msg_id and\
            reply['content']['execution_state'] == 'idle', 'bad execute iopub reply'

    if debug:
        print('---------------------------------------------------------')

## connect to the kernel

kernel = subprocess.Popen("ipython kernel", shell=True, text=True, stdout=subprocess.PIPE)

# wait for it to launch, catch the last line it prints at startup
for line in kernel.stdout:
    # print(line)
    if "--existing" in line:
        break

# get the path to JSON connection file
cf = jupyter_client.find_connection_file()
print("connecting via", cf)

client = jupyter_client.BlockingKernelClient(connection_file=cf)

# load connection info and start the communication channels
client.load_connection_file()
client.start_channels()

# handle initial chatter from the kernel

# get startup message on shell channel
reply = client.get_shell_msg()
if debug:
    print_msg(reply)

print(reply['content']['banner'])

# get two startup messages on iopub channel
io = client.get_iopub_msg()
if debug:
    print_msg(io)
assert io['msg_type'] == 'status' and\
     io['parent_header']['msg_type'] == 'kernel_info_request' and\
     io['content']['execution_state'] == 'busy', 'wrong message'

io = client.get_iopub_msg()
if debug:
    print_msg(io)
assert io['msg_type'] == 'status' and\
     io['parent_header']['msg_type'] == 'kernel_info_request' and\
     io['content']['execution_state'] == 'idle', 'wrong message'

run_cell(client, startup)


# globals
linenum = 1
indent = 0
prompt = ">>> "

# we keep a buffer of lines from the script
buffer = []

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        linenum += 1

        # add current line to end of buffer
        buffer.append(line)

        # simple logic for indentation
        newindent = len(line) - len(line.lstrip())

        if newindent == 0:
            cmd = None
            # exec last cmd
            if len(buffer) == 2:
                cmd = buffer.pop(0)

                if len(cmd) == 0:
                    print()
                elif cmd[0] == '#':
                # display the prompt
                    print(cmd)
                else:
                    if args.linenumber:
                        print(f"[{linenum:}] " + prompt + cmd)
                    else:
                        print(prompt + cmd)

            elif len(buffer) > 2:
                cmd = '\n'.join(buffer[:-1])
                if args.linenumber:
                    num = f"[{linenum:}]"
                    print(f"{num:5s} " + prompt, end='')
                else:
                    print(prompt, end='')
                for i, line in enumerate(buffer[:-1]):
                    if i > 0:
                        line = '... ' + line
                        if args.linenumber:
                            line = '      ' + line
                    print(line)
                buffer = [buffer[-1]]
                cmd += '\n'

            if cmd is not None and cmd != '':
                cmd += '\n'
                run_cell(client, cmd)


        elif newindent > indent:
            # indent has increased
            indent = newindent

        if args.maxlines is not None and linenum > args.maxlines:
            print(f'---- quitting after {args.maxlines} lines as requested!')
            break

client.shutdown()



