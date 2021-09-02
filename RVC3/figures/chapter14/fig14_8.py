#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
from spatialmath.base import plotvol3, plot_sphere

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera(name='camera 2', f=0.002, pose=T2)

F = cam1.F(cam2)

# E = cam1.E(F)
# sol = cam1.invE(E)
# inv(cam1.T) * cam2.T
# Q = [0, 0, 10]'
# cam1.project(Q)'
# cam1.move(sol[0].T).project(Q)'
# cam1.move(sol[1].T).project(Q)'
# sol = cam1.invE(E, Q)

np.random.seed(0)  # ensure repeatable results
P = SE3(-1, -1, 2) * np.random.rand(3, 20) * 2
p1 = cam1.project(P)
p2 = cam2.project(P)
# F = fmatrix(p1, p2)
# rank(F)

cam2.plot_epiline(F, p1, 'r', linewidth=0.7)
cam2.plot(P, 'bo', markersize=5)
# cam2.clf
# cam2.plot(P)
# cam2.hold
# cam2.plot_epiline(F, p1, 'r')
cam2.plot(cam1.pose.t, marker='d', markerfacecolor='k', markeredgecolor='k')

rvcprint.rvcprint(thicken=None) 
