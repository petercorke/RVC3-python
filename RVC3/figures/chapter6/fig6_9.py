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
xx = []
PP = []
lm = []
for h in ekf._history:
    x = np.linalg.norm(h.xest[:2] - map.landmark(17))
    P = np.sqrt(np.linalg.det(h.P[:2, :2]))
    #print('LM17', x, P)
    t.append(h.t)
    xx.append(x)
    PP.append(P)
    if h.lm == 17:
        lm.append(h.t)

plt.figure()
plt.subplot(211)
plt.plot(t, xx)
plt.ylabel('landmark error norm')
plt.vlines(lm, 0, 0.15)
plt.subplot(212)
plt.plot(t, PP)
plt.ylabel('landmark |P|^0.5')
plt.xlabel('time step')

plt.legend()
# rvcprint.rvcprint(subfig='a')

# plt.clf()
# ekf.show_P(ekf.P_est)

# print(np.array([h.innov for h in ekf.history]))
# rvcprint.rvcprint(subfig='b')
plt.show(block=True)

