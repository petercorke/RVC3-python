import sys
from code import InteractiveInterpreter
from io import StringIO
import contextlib
import sys
filename = "C-Chapter-02 Python.txt"
console = InteractiveInterpreter()
import code

prompt = ">>> "

init = r'''import numpy as np
from numpy.core.shape_base import _block_dispatcher
from numpy.linalg import *
import matplotlib.pyplot as plt
from math import pi, sqrt
import scipy as sp
from sympy import simplify
import mpl_toolkits.mplot3d as m3d
from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE2, SE3, Twist2, Twist3, UnitQuaternion
import matplotlib as mpl
from spatialmath import base
6 * 7
'''



for line in init.split('\n'):
    more = console.runsource(line)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# use runsource
# use re to find assignment and EOL semicolon
# halucinate a print if needed
count = 0
multiline = None
nesting = 0
with open(filename, 'r', encoding="cp1252") as f:

    for line in f:

        if line.startswith(prompt):
            print(line)

            cmd = line[4:].strip()

            with stdoutIO() as s:
                try:
                    more = console.runsource(cmd)
                    # c = code.compile_command(cmd)
                    # x = exec(c)

                except:
                    print("Something wrong with the code")

            if more:
                print("** MORE ** ", line)

            print(s.getvalue())
            # print(c, x)
            print("---------------------------")
            count += 1

            if count > 20:
                break



# def main():
#     """
#     Print lines of input along with output.
#     """
#     source_lines = (line.rstrip() for line in sys.stdin)
#     console = InteractiveInterpreter()
#     source = ''
#     try:
#         while True:
#             source = next(source_lines)
#             # Allow the user to ignore specific lines of output.
#             if not source.endswith('# ignore'):
#                 print('>>>', source)
#             more = console.runsource(source)
#             while more:
#                 next_line = next(source_lines)
#                 print('...', next_line)
#                 source += '\n' + next_line
#                 more = console.runsource(source)
#     except StopIteration:
#         if more:
#             print('... ')
#             more = console.runsource(source + '\n')


# if __name__ == '__main__':
#     main()
            