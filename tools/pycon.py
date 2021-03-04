import sys
from code import InteractiveInterpreter

def main():
    """
    Print lines of input along with output.
    """
    source_lines = (line.rstrip() for line in sys.stdin)
    console = InteractiveInterpreter()
    source = ''
    try:
        while True:
            source = next(source_lines)
            # Allow the user to ignore specific lines of output.
            if not source.endswith('# ignore'):
                print('>>>', source)
            more = console.runsource(source)
            while more:
                next_line = next(source_lines)
                print('...', next_line)
                source += '\n' + next_line
                more = console.runsource(source)
    except StopIteration:
        if more:
            print('... ')
            more = console.runsource(source + '\n')


if __name__ == '__main__':
    main()