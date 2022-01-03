#!/usr/bin/env python3

import rvcprint
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
from spatialmath.base import plotvol3, plot_sphere


T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera.Default(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera.Default(name='camera 2', f=0.002, pose=T2)

P = [0.5, 0.1, 0.8]

p1 = cam1.plot_point(P, label='point P')
p2 = cam2.plot_point(P, label='point P')

# plot epipoles
e1 = cam1.plot_point(cam2.pose.t, marker='d', markerfacecolor='k', markeredgecolor='k', label='epipole')
e2 = cam2.plot_point(cam1.pose.t, marker='d', markerfacecolor='k', markeredgecolor='k', label='epipole')

F = cam1.F(cam2)
print(F)
print(np.linalg.matrix_rank(F))
print(sp.linalg.null_space(F).T)
# e1 = h2e(ans)'
# null(F')
# e2 = h2e(ans)'

cam2.plot_epiline(F, p1, color='r', label='epipolar line')
cam1.plot_epiline(F.T, p2, color='r', label='epipolar line')

cam1._ax.legend(loc='upper right')
cam2._ax.legend(loc='upper right')

rvcprint.rvcprint(subfig='a', fignum=1, facecolor=None)
rvcprint.rvcprint(subfig='b', fignum=2, facecolor=None)
