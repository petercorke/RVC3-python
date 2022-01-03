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

p1 = cam2.project_point(P)
p2 = cam2.project_point(P)
H, _ = CentralCamera.points2H(p1, p2)

p1b = smb.homtrans(np.linalg.inv(H), p2)
Q = np.array([
        [-0.2302,   -0.0545,    0.2537],
        [ 0.3287,    0.4523,    0.6024],
        [ 0.4000,    0.5000,    0.6000]
    ])
smb.plotvol3([-1, 1, -1, 1, -0.2, 1.8])
smb.plot_sphere(centre=P, radius=0.05, color='b')
smb.plot_sphere(centre=Q, radius=0.05, color='r')

cam1.plot(color='b', shape='camera', frame=True, scale=0.15, alpha=0.7)
cam2.plot(color='r', shape='camera', frame=True, scale=0.15, alpha=0.7)
plt.gca().view_init(13, -114)

rvcprint.rvcprint(interval=(0.5, 1, 0.25), facecolor='w')
