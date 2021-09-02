#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
import spatialmath.base as smb

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera(name='camera 2', f=0.002, pose=T2)

Tgrid = SE3(0, 0, 1) * SE3.Rx(0.1) * SE3.Ry(0.2)
P = mkgrid(3, 1.0, pose=Tgrid)

p1 = cam1.plot(P, 'ko', markerfacecolor='w')
p2 = cam2.plot(P, 'ko', markerfacecolor='w')

H, _ = CentralCamera.HfromPoints(p1, p2)
print(H)
p2b = smb.homtrans(H, p1)
cam2.plot(p2b, 'k+')

rvcprint.rvcprint(subfig='a', fignum=1)
rvcprint.rvcprint(subfig='b', fignum=2)
