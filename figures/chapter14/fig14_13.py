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
cam1 = CentralCamera(name='camera 1', f=0.002, imagesize=1000, rho=10e-6, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera(name='camera 2', f=0.002, imagesize=1000, rho=10e-6, pose=T2)


Tgrid = SE3(0, 0, 1) * SE3.Rx(0.1) * SE3.Ry(0.2)
P = mkgrid(3, 1.0, pose=Tgrid)

p1 = cam1.project_point(P)
p2 = cam2.project_point(P)
H, _ = CentralCamera.points2H(p1, p2)
print(H)

Q = np.array([
        [-0.2302,   -0.0545,    0.2537],
        [ 0.3287,    0.4523,    0.6024],
        [ 0.4000,    0.5000,    0.6000]
    ])

# p1 = cam1.plot_point(np.hstack((P, Q)), 'ko', markerfacecolor='w')
p1 = cam1.plot_point(P, 'bo', markerfacecolor='w', label='projected in-plane point')
q1 = cam1.plot_point(Q, 'ro', markerfacecolor='w', label='projected out-of-plane point')
cam1._ax.legend()
rvcprint.rvcprint(subfig='a', facecolor=None)

# p2 = cam2.plot_point(np.hstack((P, Q)), 'ko', markerfacecolor='w')
cam2.plot_point(P, 'bo', markerfacecolor='w', label='projected in-plane point')
cam2.plot_point(Q, 'ro', markerfacecolor='w', label='projected out-of-plane point')
p2h = smb.homtrans(H, p1)
q2h = smb.homtrans(H, q1)
cam2.plot_point(p2h, 'b+', label='in-plane point transformed from image 1')
cam2.plot_point(q2h, 'r+', label='out-of-plane point transformed from image 1')
cam2._ax.legend()

rvcprint.rvcprint(subfig='b', facecolor=None)
