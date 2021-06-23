#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *


# EKF map making

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(0.5)]) ** 2
W = np.diag([0.01, np.radians(1)]) ** 2

veh = Bicycle(animation='car', workspace=10)  # error free vehicle
veh.control = RandomPath(workspace=veh.workspace)

map = LandmarkMap(nlandmarks=20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W)

ekf = EKF(robot=(veh, None), P0=P0, sensor=(sensor, 10*W), verbose=True)
print(ekf)


ekf.run(T=100)

map.plot()
ekf.plot_map(filled=True, color='g')
veh.plot_xy('b')

"""
some landmark error seen here and in SLAM
no error if W=0
initial error in landmark estimate that never goes away
cannot be error in xv prediction since it happens for map making case
covariance is also very small

need to look at history of estimated position and its covariance
"""
print(ekf._landmarks[:,0])
lm_id = 0
ix = ekf._landmarks[0,lm_id]
l1 = np.array([tuple(h.xest[ix:ix+2]) for h in ekf.history[9:]])
lmerr = np.linalg.norm(l1 - ekf.sensor.map.landmark(lm_id), axis=1)

# rvcprint.rvcprint(subfig='a', debug=True)

# plt.clf()
# ekf.show_P()

# print(np.array([h.innov for h in ekf.history]))
# # rvcprint.rvcprint(subfig='b', 'opengl')
plt.show(block=True)

