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
cam1 = CentralCamera.Default(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera.Default(name='camera 2', f=0.002, pose=T2)

Tgrid = SE3(0, 0, 1) * SE3.Rx(0.1) * SE3.Ry(0.2)
P = mkgrid(3, 1.0, pose=Tgrid)

p1 = cam1.plot_point(P, 'ko', markerfacecolor='w')
p2 = cam2.plot_point(P, 'ko', markerfacecolor='w')

H, _ = CentralCamera.points2H(p1, p2)
print(H)
p2b = smb.homtrans(H, p1)
cam2.plot_point(p2b, 'k+')

cam1._ax.legend(['projected point'], facecolor='w')
cam2._ax.legend(['projected point', 'point transformed from image 1'], facecolor='w')
rvcprint.rvcprint(subfig='a', fignum=1, facecolor=None)
rvcprint.rvcprint(subfig='b', fignum=2, facecolor=None)
