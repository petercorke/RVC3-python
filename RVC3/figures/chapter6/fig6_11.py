#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *

# EKF SLAM
map = LandmarkMap(nlandmarks=20, workspace=10)

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V)
veh.control = RandomPath(workspace=map.workspace)

sensor = RangeBearingSensor(veh, map, covar=W, animate=True, range=6,
    angle=[-np.pi/2, np.pi/2], verbose=True)
ekf = EKF(robot=(veh, V), P0=P0, sensor=(sensor, W), verbose=True)
print(ekf)


ekf.run(T=80) #40

veh.plot_xy('b', label='ground truth')
ekf.plot_xy('r', label='EKF estimate')
# ekf.plot_map(filled=True, color='g', alpha=0.5)
plt.legend()
for i in range(19):
    x = ekf._x_est[i*2:i*2+2]
    plt.plot(x[1], x[0], '+')

# rvcprint.rvcprint()
plt.show(block=True)