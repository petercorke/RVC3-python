#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from matplotlib.ticker import ScalarFormatter
from spatialmath.base import plotvol2

# EKF localization with landmarks

map = LandmarkMap(20, workspace=10)
print(map)

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([.05, .05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2
x0 = [0, 0, 0]

veh = Bicycle(covar=V, x0=x0, seed=0, animation=None)
veh.control = RandomPath(workspace=map.workspace, seed=0)


P0 = np.diag([0.005, 0.005, 0.001]) ** 2

sensor = RangeBearingSensor(veh, map, covar=W, animate=True, 
    angle=[-np.pi/2, np.pi/2], range=4, verbose=True)
print(sensor)
ekf = EKF(robot=(veh, V), P0=P0, map=map, sensor=(sensor, W), animate=False)
print(ekf)

ekf.run(T=20)

# map.plot()
ekf.plot_ellipse(filled=True, N=20, facecolor='g', alpha=0.3, edgecolor='none')

veh.plot_xy(color='b', linewidth=2, label='ground truth')
ekf.plot_xy('r', linewidth=2, label='EKF estimate')
plt.legend() #['ground truth', 'EKF estimate'])

v = VehiclePolygon('car')
v.plot(x0, facecolor='none', edgecolor='k')

rvcprint.rvcprint(subfig='a', thicken=None)

ax = plt.gca()
ax.set_xlim(-3.5, -1.5)
ax.set_ylim(0, 2)



rvcprint.rvcprint(subfig='b', thicken=None)


