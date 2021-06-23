#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from matplotlib.ticker import ScalarFormatter

# EKF localization
V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([.05, .05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, animation='car', workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

# odo = veh.step(1, 0.3)
# odo = veh.step(1, 0.3)
print(veh)
# veh.run(10)

Fx = veh.Fx([0, 0, 0], [0.5, 0.1])
print(Fx)

P0 = np.diag([0.005, 0.005, 0.001]) ** 2

map = LandmarkMap(nlandmarks=20)
print(map)

sensor = RangeBearingSensor(veh, map, covar=W, animate=True, 
    angle=[-np.pi/2, np.pi/2], range=4, verbose=True)
print(sensor)
ekf = EKF(robot=(veh, V), P0=P0, map=map, sensor=(sensor, W))
print(ekf)

ekf.run(T=20)

ekf.plot_ellipse(filled=True, N=20, facecolor='g', alpha=0.3, edgecolor='none', label='_uncertainty')

veh.plot_xy(color='b', linewidth=2, label='ground truth')
ekf.plot_xy('r', linewidth=2, label='EKF estimate')
plt.legend() #['ground truth', 'EKF estimate'])

rvcprint.rvcprint(subfig='a', thicken=None)

ax = plt.gca()
ax.set_xlim(-2, 2.2)
ax.set_ylim(2, 6)


rvcprint.rvcprint(subfig='b', thicken=None)

