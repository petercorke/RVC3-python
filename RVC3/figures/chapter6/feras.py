#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *


# EKF map making

W = np.diag([0.01, np.radians(1)]) ** 2

map = LandmarkMap(nlandmarks=20, workspace=10)

veh = Bicycle()  # error free vehicle
veh.control = RandomPath(workspace=map.workspace)

sensor = RangeBearingSensor(veh, map, covar=W)

map.plot()
ekf = EKF(robot=(veh, None), sensor=(sensor, 10*W), joseph=False, verbose=False)
print(ekf)

# test Hp
# xv = [1, 2, 1]
# z = sensor.h(xv, 17)
# print(z)
# xf = map.landmark(17)
# print(xf)

# z = sensor.h(xv, xf)
# print(z)

# print(sensor.Hp(xv, 17))

# print((sensor.h(xv, xf+[0.001, 0]) - z) / 0.001)
# print((sensor.h(xv, xf+[0, 0.001]) - z) / 0.001)

ekf.run(T=100)


print(np.sqrt(np.var(ekf.xxdata[0])))
print(np.sqrt(np.var(ekf.xxdata[0])))


print(ekf.landmark(6))

ekf.plot_map(filled=True, color='g')
veh.plot_xy('b', label='true path')
map.plot(labels=True)

"""
some landmark error seen here and in SLAM
no error if W=0
initial error in landmark estimate that never goes away
cannot be error in xv prediction since it happens for map making case
covariance is also very small

need to look at history of estimated position and its covariance
"""
# print(ekf._landmarks[:,0])
# lm_id = 0
# ix = ekf._landmarks[0,lm_id]
# l1 = np.array([tuple(h.xest[ix:ix+2]) for h in ekf.history[9:]])
# lmerr = np.linalg.norm(l1 - ekf.sensor.map.landmark(lm_id), axis=1)
# print(lmerr)

t = []
xv = []
PP = []
lm = []
z = []
for h in ekf._history:
    t.append(h.t)
    lm.append(h.lm)
    z.append(h.z)

t = np.array(t)
lm = np.array(lm)
z = np.array(z)
xv = np.array(veh._x_hist)

import scipy.io

mdict = dict(t=t, lm=lm, z=z, xv=xv, W=W, map=map._map.T)

scipy.io.savemat('peter_ekf.mat', mdict, oned_as='column')