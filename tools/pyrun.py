import sys

import contextlib
import re
import argparse
from subprocess import Popen, PIPE
from threading  import Thread
from queue import Queue, Empty
import time

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
parser.add_argument('--comments', '-c', 
        action='store_const', const=True, default=False,
        help='show comments, default %(default)s')
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

# handle async i/o from subprocess.  stdout goes to a queue

# https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python

def enqueue_output(out, queue):
    try:
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
    except ValueError:
        pass

ON_POSIX = 'posix' in sys.builtin_module_names


# regexps to remove IPython output, easier than changing the prompts
re_in = re.compile(r'In \[[0-9]+\]:')
re_out = re.compile(r'Out\[[0-9]+\]:')
re_contin = re.compile(r'\.\.\.:')

def print_available(q):
    while True:
        try:
            line = q.get(timeout=args.timeout)
        except Empty:
            break

        line = line.decode('utf8').rstrip()
        line = re_in.sub('', line)
        line = re_out.sub('', line)
        line = re_contin.sub('', line)
        if len(line) > 2 and line[0] == ' ' and line[1] == ' ':
            line = line[2:]

        if len(line) > 0:
            print(line)   

# globals
linenum = 1
indent = 0
prompt = ">>> "

with open(filename, 'r') as f, \
     Popen('ipython', stdin=PIPE, stdout=PIPE, bufsize=0, close_fds=ON_POSIX) as p:

    # create thread to read stdout from subprocess and a queue
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()

    # give IPython a moment to startup
    time.sleep(1)

    # give it the initialization commands
    p.stdin.write(startup.encode('utf8'))
    print_available(q)


    # we keep a buffer of lines from the script
    buffer = []

    for line in f:
        line = line.rstrip()
        linenum += 1

        if len(line) == 0:
            print()
        elif line[0] == '#':
            if args.comments:
                print(line)
            line = ''
            continue

        # add current line to end of buffer
        buffer.append(line)

        # simple logic for indentation
        newindent = len(line) - len(line.lstrip())

        if newindent == 0:
            cmd = None
            # exec last cmd
            if len(buffer) == 2:
                cmd = buffer.pop(0)
                # display the prompt
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
                p.stdin.write(cmd.encode('utf8'))

            print_available(q)

        elif newindent > indent:
            # indent has increased
            indent = newindent

        if args.maxlines is not None and linenum > args.maxlines:
            print(f'---- quitting after {args.maxlines} lines as requested!')
            break
    time.sleep(1)
    print_available(q)
