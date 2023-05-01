#! /usr/bin/env python3

import subprocess
import sys
import re
import os
import os.path
import argparse
from subprocess import Popen, PIPE
from threading  import Thread
from queue import Queue, Empty
from  colored import fg, bg, attr
import copy
from collections import Counter
import textwrap
import shutil
from pathlib import Path



debug = False
tagcount = Counter()
nerrors = 0
ncells = 0
nlistings = 0
linenum = 0

# we keep a buffer of lines from the script
buffer = []
inline = False

last_result = []

lastsection = ''

re_section = re.compile(r'^\\(?:sub)*section{([^}]+)')
re_space = re.compile(r'\s+')

# handle command line arguments
parser = parser = argparse.ArgumentParser(description='Run Python script for RVC3 book.')
parser.add_argument('texfile', 
        default=None, nargs='?',
        help='the script to run')


# things to show
parser.add_argument('--matlab', '-M', 
        action='store_const', const=True, default=False, dest='matlab',
        help='parse MATLAB code, default %(default)s')

parser.add_argument('--cell', '-c', 
        action='store_const', const=True, default=False, dest='show_cell',
        help='show code cells from file (blue), default %(default)s')
parser.add_argument('--result', '-r', 
        action='store_const', const=True, default=False, dest='show_cell_results',
        help='show results from Python/MATALAB (green), default %(default)s')
parser.add_argument('--file', '-f', 
        action='store_const', const=True, default=False, dest='show_file_results',
        help='show results from file (light blue), default %(default)s')
parser.add_argument('--diff', '-d', 
        action='store_const', const=True, default=False, dest='show_diff',
        help='show results when different %(default)s')
parser.add_argument('--script', '-S', 
        action='store_const', const=True, default=False, dest='script',
        help='write python script %(default)s')
# creating new file
parser.add_argument('--replace', '-R', 
        action='store_const', const=True, default=False, dest='replace_results',
        help='replace code cell results in .tex file, default %(default)s')
parser.add_argument('--output', '-o', 
        action='store_const', const=True, default=False, dest='write_tex',
        help='copy input .tex file to .output -py.tex, default %(default)s')
parser.add_argument('--nocolor',
        action='store_const', const=False, default=True, dest='color',
        help='no colorization of results, default %(default)s')

parser.add_argument('--plot', '-P', 
        action='store_const', const=True, default=False, dest='show_plots',
        help='display plots, default %(default)s')

parser.add_argument('--maxlines', '-m', 
        type=int, default=None,
        help='maximum number of lines to read, default %(default)s')
parser.add_argument('--start', type=int, default=1, dest='start_cell',
        help='cell to commence at, base 1, %(default)s')
parser.add_argument('--continue', '-C',
        action='store_const', const=False, default=True, dest='stop_on_error',
        help='stop at first error, default %(default)s')

parser.add_argument('--linenumber', '-l', 
        default=False, action='store_const', const=True,
        help='show line numbers, default %(default)s')
parser.add_argument('--traceback', '-t', 
        action='store_const', const=False, default=True, dest='show_traceback',
        help='skip full error traceback, default %(default)s')
parser.add_argument('--sections', '-s', 
        action='store_const', const=True, default=False, dest='show_sections',
        help='show sections, default %(default)s')
parser.add_argument('--debug', '-D', 
        action='store_const', const=True, default=False, dest='debug',
        help='debugging, default %(default)s')

parser.add_argument('--timeout',
        type=float, default=0.2,
        help='timeout on each IPython command, default %(default)s seconds')
parser.add_argument('--quiet', '-q',
        action='store_const', const=True, default=False, dest='only_errors',
        help='only show error reports, default %(default)s')

args = parser.parse_args()

os.system("clear")

root = Path(__file__).absolute().parent.parent / "RVC3"
sys.path.append(str(root / "models"))
sys.path.append(str(root / "examples"))

def cprint(color, str, **kwargs):
    if str is not None:
        print(fg(color) + str + attr(0), **kwargs)

def c2print(fgcolor, bgcolor, str, **kwargs):
    if str is not None:
        print(fg(fgcolor) + bg(bgcolor) +  str + attr(0), **kwargs)

def flag_error(offset=0):
    c2print('white', 'red', f'\nERROR #{nerrors} at line {linenum-offset}:')

debug = args.debug
if args.texfile is None:
    print('no file specified')
    sys.exit(1)
else:
    filename = args.texfile

out = None
if args.write_tex:
    out_tex = open(os.path.splitext(filename)[0] + '-py.tex', 'w')

process_cells = False

if not args.matlab:

    import jupyter_client
    import base64
    from PIL import Image
    import io

    class ExecutePython:

        def __init__(self, plots=False):
            ## connect to the kernel

            kernel = subprocess.Popen("ipython kernel", shell=True, text=True, stdout=subprocess.PIPE)

            # wait for it to launch, catch the last line it prints at startup
            for line in kernel.stdout:
                if debug:
                    print('kernel startup: ', line.rstrip())
                if "--existing" in line:
                    break

            # get the path to JSON connection file
            cf = jupyter_client.find_connection_file()
            if debug:
                print("connecting via", cf)

            client = jupyter_client.BlockingKernelClient(connection_file=cf)

            if debug:
                print("connected")
            # load connection info and start the communication channels
            client.load_connection_file()
            client.start_channels()

            if debug:
                print('channel started')

            self.client = client

            self.figcount = 0
            self.plots = plots
            if plots:
                try:
                    shutil.rmtree('./PLOTS')
                except FileNotFoundError:
                    pass
                os.mkdir('./PLOTS')

        @staticmethod
        def print_msg(m, indent=0):
            for k, i in m.items():
                if isinstance(i, dict):
                    print(' ' * indent, f"{k}::")
                    IPython.print_msg(i, indent+4)
                else:
                    s = f"{k:10s}: {i}"
                    if len(s) > 100:
                        s = s[:100]
                    print(' ' * indent, s)
            if indent == 0:
                print()


        def read_message(self, channel, msg_type=None, exec_state=None):

            while True:
                if channel == 'shell':
                    reply = self.client.get_shell_msg()
                elif channel == 'iopub':
                    reply = self.client.get_iopub_msg()

                if debug:
                    print(f'reading on {channel} channel')
                    IPython.print_msg(reply)

                if reply['parent_header']['msg_id'] != self.msg_id:
                    if debug:
                        print('message not requested')
                    continue

                if msg_type is not None and reply['msg_type'] != msg_type:
                    IPython.print_msg(reply)
                    raise AssertionError('incorrect msg_type')

                if exec_state is not None and reply['content']['execution_state'] != exec_state:
                    IPython.print_msg(reply)
                    raise AssertionError('incorrect execution_state')

                return reply


        def run_cell(self, code):
            global nerrors, ncells

            ncells += 1
            
            # now we can run code.  This is done on the shell channel

            # execution is immediate and async, returning a UUID
            msg_id = self.client.execute(code, silent=False)
            self.msg_id = msg_id

            if debug:
                print(f"\nrunning: {code}\n  msg_id = {msg_id}\n")

            # # there is one response message which tells how it went
            reply = self.read_message('shell', 'execute_reply')

            result = []
            status = reply['content']['status']
            if status == 'ok':
                # server produced a result, process it

                # first message says busy
                reply = self.read_message('iopub', 'status', 'busy')

                # second message is execute_input which reflects back the command
                reply = self.read_message('iopub', 'execute_input')

                while True:
                    # iterate on messages
                    reply = self.client.get_iopub_msg()
                    if debug:
                        self.print_msg(reply)
                    
                    # check it is a reply to this transaction
                    assert reply['parent_header']['msg_id'] == msg_id, 'bad execute iopub reply'

                    # check for last message in response sequence
                    if reply['msg_type'] == 'status' and\
                            reply['content']['execution_state'] == 'idle':
                        break

                    if reply['msg_type'] == 'stream':
                        # command had an output
                        if not args.only_errors:
                            result.extend(reply['content']['text'].split('\n'))
                    elif reply['msg_type'] == 'execute_result':
                        # command had an output
                        if not args.only_errors:
                            result.extend(reply['content']['data']['text/plain'].split('\n'))
                            if debug:
                                print('RESULT', result)
                    elif reply['msg_type'] == 'display_data':
                        # command created graphical  data
                        # try:
                        #     img_data = reply['content']['data']['image/png']
                        # except KeyError:
                        #     self.print_msg(reply)
                        #     raise AssertionError
                        # img = Image.open(io.BytesIO(base64.b64decode(img_data)))
                        # global linenum, lastsection
                        # if self.plots:
                        #     # img.show(title=f"line #{linenum}")
                        #     img.save(f"./PLOTS/fig-{linenum}.png")
                        pass
                
                # get rid of stray trailing blank line
                if len(result) > 0 and result[-1] == "":
                    del result[-1]


            elif status == 'error':
                # server produced an error, display it

                # first message says busy
                reply = self.read_message('iopub', 'status', 'busy')

                # second message is execute_input which reflects back the command
                reply = self.read_message('iopub', 'execute_input')

                # third message is command display value
                
                # skip possible display data message
                while True:
                    reply = self.read_message('iopub')
                    if reply['msg_type'] == 'error':
                        break

                flag_error(-2)
                
                for line in reply['content']['traceback']:
                    if args.show_traceback:
                        print('        ' + line.replace('\n', '\n        '))

                while True:
                    # flush messages till idle
                    # fourth message is execute_input which reflects back the command
                    reply = self.client.get_iopub_msg()
                    if debug:
                        print_msg(reply)
                    if reply['msg_type'] == 'status' and \
                        reply['parent_header']['msg_id'] == msg_id and \
                        reply['content']['execution_state'] == 'idle':
                            break
                nerrors += 1
            
                result = None

            if debug:
                print('---------------------------------------------------------')

            return result

        def shutdown(self):
            self.client.shutdown()

        def startup(self):
            # initial commands pushed to IPython
            startup = textwrap.dedent(r"""
                %config InteractiveShell.ast_node_interactivity = 'last_expr_or_assign'
                import numpy as np
                import scipy as sp
                import matplotlib.pyplot as plt
                import cv2 as cv

                import ansitable
                ansitable.options(unicode=True)

                from spatialmath import *
                from spatialmath.base import *
                BasePoseMatrix._color=False
                from roboticstoolbox import *

                from spatialmath.base import *
                import math
                from math import pi

                from machinevisiontoolbox import *
                from machinevisiontoolbox.base import *

                %precision %.4g
                np.set_printoptions(
                    linewidth=120, formatter={
                        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

                np.random.seed(0)
                cv.setRNGSeed(0)
                """)

            self.run_cell(startup)

    prompt = ">>> "
    prompt_contin = "... "
    prompt_wrong = [">> ", "...: "]

    
    server = ExecutePython(args.show_plots)
    
else:

    import matlab.engine

    class ExecuteMATLAB:

        def __init__(self):
            self.engine = matlab.engine.start_matlab('-desktop')  #matlab.engine.connect_matlab()
            print('MATLAB engine started')

        def run_cell(self, code):
            print(linenum, code)
            z = self.engine.evalc(code)
            print(z)
            return z

        def shutdown(self):
            self.engine.quit()

        def startup(self):
            # initial commands pushed to MATLAB
            startup = textwrap.dedent(r"""
                addpath(genpath("~/Dropbox/code/MATLAB/RVC3-MATLAB/newtoolbox"));
                ver
                """)

            self.run_cell(startup)

    server = ExecuteMATLAB()

    prompt = ">> "
    prompt_contin = ">> "
    prompt_wrong = [">>> "]

server.startup()

def getline():
    """
    Read next line from the file

    Yields:
        str: line from file

    Lines have no newlines
    """
    global linenum, lastsection, out_py

    with open(filename, 'r') as f:
        for line in f:
            linenum += 1

            m = re_section.match(line)
            if m is not None:
                lastsection = copy.copy(line)
                if args.show_sections:
                    print()
                    c2print('black', 'yellow', line)
                if args.script:
                    print('\n# ' + m.group(1) + '\n' ,file=out_py)

            yield line.rstrip()

def getlisting():
    """
    Return contents of a lstlisting environment

    Yields:
        list of str: string comprising lstlisting body
    """
    global nlistings, process_cells

    inlisting = False
    tags = []
    buffer = []

    for line in getline():
        inlisting_new = None

        sline = line.lstrip()
        if sline.startswith('%%TAG:'):
            tag = sline[6:]
            # this magic comment applies to the next lstlisting env encountered
            tags.append(tag)
            tagcount[tag] += 1

        if sline.startswith(r'\begin{lstlisting}'):
            nlistings += 1
            if nlistings >= (args.start_cell):
                process_cells = True
            if process_cells and len(tags) == 0:
                inlisting_new = True

        if sline.startswith(r'\end{lstlisting}'):
            if process_cells and len(tags) == 0:
                inlisting_new = False
            tags = []

        # change state
        if inlisting_new is False:
            # at the end of a lstlisting block

            yield buffer
            buffer = []
            inlisting = False
        
        if inlisting:
            if 'NOBLOCK' in tags:
                line = line.replace(".disp()", ".disp(block=False)")
            buffer.append(line)
        elif args.write_tex:
            print(line, file=out_tex)
        
        if inlisting_new:
            inlisting = inlisting_new

def getblocks():
    """
    Return code or results from lstlisting environment

    Yields:
        tuple: (blocktype, blocktext)

    blocktype is either 'code' or 'result'. The text is a (multiline) string containing congiguous lines that are
    either code (starts with a prompt or continuation) or results.
    """

    def stripprompt(s):
        return s[len(prompt):]

    for listing in getlisting():
        buffer = []
        lstenv = []
        while len(listing) > 0:
            line = listing.pop(0)

            # check for wrong prompt in this language
            for wp in prompt_wrong:   
                if line.startswith(wp):
                    flag_error()
                    print('wrong prompt', wp)
                    continue

            # group of lines
            if line.startswith(prompt):
                # prompt line
                buffer = [line]

                # add continuation lines
                while len(listing) > 0 and listing[0].startswith(prompt_contin):
                    buffer.append(listing.pop(0))

                lstenv.append(('code', '\n'.join([stripprompt(l) for l in buffer]), '\n'.join(buffer)))
            else:
                # results line
                buffer = [line]
                # add results lines
                while len(listing) > 0 and not listing[0].startswith(prompt):
                    buffer.append(listing.pop(0))

                lstenv.append(('result', '\n'.join(buffer), None))
        yield lstenv

# globals
linenum = 1
indent = 0


def main():

    nmismatch = 0

    result = None

    for listenv in getblocks():
        for i, (type, block, code) in enumerate(listenv):
            # for every code or result chunk

            # print(type, block)

            if type == 'code':
                # this is executable code

                if args.write_tex:
                    print(code, file=out_tex)

                if args.script:
                    c = code.replace(prompt, '')
                    c = c.replace(prompt_contin, '')
                    print(c, file=out_py) # strip off prompt
                    continue

                if args.show_cell:
                    cprint('blue', block)

                # send it to IPython to execute
                result = server.run_cell(block)

                # result is a list of strings or None if error
                if args.show_cell_results and result is not None:
                    if args.color:
                        cprint('yellow', '\n'.join(result))  # Python result
                    else:
                        print('\n'.join(result))

                if result is None:
                    if args.stop_on_error:
                        break
                    else:
                        continue
                else:
                    result = '\n'.join(result)

                # is there a result left over from last block?
                if result is not None and (
                        i == (len(listenv) - 1) or 
                        ((i < len(listenv) - 1) and listenv[i+1][0] == 'code')
                        ):
                    # next block is also code, spit the result now
                    if args.replace_results and result != '':
                        # replace results in output stream
                        print(result, file=out_tex)

            elif type == 'result':
                # this is a code result from the file
            
                # display the current line
                if args.show_file_results:
                    cprint('sky_blue_3', block)  # book version
                    if args.show_cell_results:
                        print()

                if args.write_tex:
                    if args.replace_results:
                        # replace results in output stream
                        print(result, file=out_tex)
                    else:
                        # use old results
                        print(block, file=out_tex)

                # check for differences
                if result is None:
                    res1 = ''
                else:
                    res1 = re_space.sub('', result)
                res2 = re_space.sub('', block)
                if res1 != res2:
                    # strings are different
                    nmismatch += 1
                    if args.show_sections:
                        print()
                        c2print('black', 'white', lastsection.strip())
                    if args.show_diff:
                        cprint('sky_blue_3', block)  # book version
                        if not args.show_cell_results:
                            cprint('yellow', result)     # Python result
                        print(f'^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ at line {linenum}\n')
                    
        if result is None and args.stop_on_error and not args.script:
            break
        if args.maxlines is not None and linenum > args.maxlines:
            print(f'---- quitting after {args.maxlines} lines as requested!')
            break

    server.shutdown()

    if args.script:
        print("--> ", out_py.name)

    if args.write_tex:
        print("--> ", out_tex.name)


    print(f"{args.texfile}:: processed {linenum} lines, {nlistings} lstlisting blocks, {ncells} cells, with {nmismatch} mismatched results and {nerrors} errors")

    print(tagcount)


if args.script:
    out_py = open(os.path.splitext(filename)[0] + '.py', 'w')
    print("# ------ standard imports ------ #", file=out_py)
    for line in startup_python.split('\n'):
        if len(line) > 0 and line[0] in "%#":
            continue
        print(line, file=out_py)
    print("# ------------------------------ #\n", file=out_py)

if __name__ == "__main__":
    main()
    sys.exit(nerrors)
