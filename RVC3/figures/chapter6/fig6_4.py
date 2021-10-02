#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from spatialmath.base import plotvol2

# EKF dead reckoning
x0 = [0, 0, 0]
V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([.05, .05, np.radians(0.5)]) ** 2

veh = Bicycle(covar=V, workspace=10, x0=x0, seed=0, animation=None) #,animation='car')
veh.control = RandomPath(workspace=veh.workspace, seed=0)

P0 = np.diag([0.005, 0.005, 0.001]) ** 2
ekf = EKF(robot=(veh, V), P0=P0, animate=False)

ekf.run(T=20, animate=False)

plotvol2(10)
ekf.plot_ellipse(filled=True, facecolor='g', alpha=0.3, edgecolor='none', label='_uncertainty')

veh.plot_xy(color='b', linewidth=2, label='ground truth')
ekf.plot_xy('r', linewidth=2, label='EKF estimate')
plt.legend() #['ground truth', 'EKF estimate'])

v = VehiclePolygon('car')
v.plot(x0, facecolor='none', edgecolor='k')

rvcprint.rvcprint()

