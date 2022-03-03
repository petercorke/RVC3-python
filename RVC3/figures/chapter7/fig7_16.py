#!/usr/bin/env python3

from roboticstoolbox import *
import rvcprint
from roboticstoolbox.backends.swift import Swift
from spatialmath import SE3
import time
from pathlib import Path

root = Path('~/Downloads').expanduser()

swift = Swift()
swift.launch()

ur5 = models.URDF.UR5()

swift.add(ur5)
ur5.q = [0, -1.1, 1.4, -0.6, 0.4, 0.4]

p = 1
swift.set_camera_pose([1.2, 0.5, 0.2], [0, 0, 0.2])
swift.step()

time.sleep(0.4)

filename = 'swift_snap'
swift.screenshot(filename)
time.sleep(4)


file = root / filename
target = Path(rvcprint.outfile(subfig='a', format='png'))
file.with_suffix('.png').rename(target)

swift.close()

time.sleep(2)

# ------------------------------------------------------------------------ #
swift = Swift()
swift.launch()

yumi = models.URDF.YuMi()
swift.add(yumi)
yumi.q = yumi.q1

p = 1
# swift.set_camera_pose([p, 0.03, p], [0, 0, 0.2])
swift.set_camera_pose([p, 0.2, .6], [0, 0, 0.3])

swift.step()

time.sleep(0.4)

filename = 'swift_snap'
swift.screenshot(filename)
time.sleep(4)

root = Path('~/Downloads').expanduser()

file = root / filename
target = Path(rvcprint.outfile(subfig='b', format='png'))
file.with_suffix('.png').rename(target)
