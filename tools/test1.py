import code
from code import InteractiveInterpreter
from io import StringIO
import contextlib
import sys

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


cmd = "for i in range(10):"

c = code.compile_command(cmd)
print(c)

cmd = "  print(i)"

c = code.compile_command(cmd)
print(c)

# console = InteractiveInterpreter()

# # x = console.runcode(code=c)
# print('----')
# x = exec(c)
# print('----')

# print(x)

print('----')


with stdoutIO() as s:
    try:
        x = exec(c)

    except:
        print("Something wrong with the code")

print('----')
print("out:", s.getvalue())
