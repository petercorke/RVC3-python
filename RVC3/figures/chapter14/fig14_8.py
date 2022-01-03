#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera.Default(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera.Default(name='camera 2', f=0.002, pose=T2)

F = cam1.F(cam2)

E = cam1.E(F)
sol = cam1.decomposeE(E)
sol.printline(orient='camera')
cam1.pose.inv() * cam2.pose
Q = [0, 0, 10]
q1 = cam1.project_point(Q, pose=sol[2]).T

for i in range(4):
    print(cam1.project_point(Q, pose=sol[i]))

sol = cam1.decomposeE(E, Q)

np.random.seed(0)  # ensure repeatable results
P = SE3(-1, -1, 2) * np.random.rand(3, 20) * 2
p1 = cam1.project_point(P)
p2 = cam2.project_point(P)
# F = fmatrix(p1, p2)
# rank(F)

cam2.plot_point(P, 'ko', markersize=5)
# cam2.clf
# cam2.plot(P)
# cam2.hold
# cam2.plot_epiline(F, p1, 'r')
cam2.plot_point(cam1.pose.t, marker='d', markerfacecolor='k', markeredgecolor='k')
cam2.plot_epiline(F, p1, 'r', linewidth=0.7)

plt.legend(['point P', 'epipole', 'epipolar line'])

rvcprint.rvcprint(thicken=None, facecolor=None) 
