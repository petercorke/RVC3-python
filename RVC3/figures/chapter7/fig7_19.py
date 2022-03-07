#!/usr/bin/env python3

from roboticstoolbox import *

from roboticstoolbox.backends.swift import Swift
from pathlib import Path
from rvcprint import outfile
import time

root = Path('~/Downloads').expanduser()

# cleanup old files
for file in root.glob('swift_snap*.png'):
    print('removing ', file)
    file.unlink()

poses = [('lu', 'a'), ('ru', 'b'), ('ld', 'c'), ('rd', 'd')]

swift = Swift()
swift.launch()

puma = models.URDF.Puma560()

ee = puma.fkine(puma.configs['lu']).t

# print(puma)

swift.add(puma)

# from to
swift.set_camera_pose([1.3, 0, ee[2]], ee)

for config, subfig in poses:
    puma.q = puma._configs[config]
    swift.step()
    time.sleep(0.5)
    swift.screenshot('swift_snap')

    time.sleep(4)

    file = root / 'swift_snap'
    target = Path(outfile(subfig=subfig, format='png'))
    # file.with_suffix('.png').rename(target)

# this is showing wrong configurations

