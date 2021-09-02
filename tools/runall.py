#!/usr/bin/env python3

import sys
import os
import argparse
import runpy
import subprocess
from colored import fg, attr

parser = argparse.ArgumentParser(description='Run RVC figure files.')
parser.add_argument('--verbose', '-v', dest='verbose', action='store_const',
                    const=True, default=False,
                    help='show script outputs')
parser.add_argument('--print', '-p', dest='print', action='store_const',
                    const=True, default=False,
                    help='enable rvcprint in scripts')
parser.add_argument('--bdsim', '-b', dest='bdsim', action='store_const',
                    const=True, default=False,
                    help='disable bdsim graphics')
parser.add_argument('files', nargs='*',
                    help='files to process')
args = parser.parse_args()

env = os.environ
if args.print:
    env['RVCPRINT'] = 'yes'
else:
    env['RVCPRINT'] = 'no'

failed = []
for file in args.files:
    print(f"{file:<12s}: ", end="", flush=True)
    cmd = [file]
    if args.bdsim:
        cmd.append('--nographics')
    try:
        result = subprocess.run(cmd, capture_output=True, env=env)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print(f"subprocess spawn of {file} failed")
        continue
    if result.returncode == 0:
        print('OK')
    else:
        print('FAILED')
        failed.append(file)
        if args.verbose:
            print('return code was', result.returncode)
            print(result.stdout.decode('utf-8'))
            print(fg('red') + result.stderr.decode('utf-8') + attr('reset'))

print('\n-------------------------------------------------------------')
print(f"{len(args.files)} files processed", end='')
if len(failed) > 0:
    print(f", {len(failed)} failed")
    for file in failed:
        print('  ', file)
else:
    print()