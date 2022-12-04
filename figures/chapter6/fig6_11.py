#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *


# EKF map making

W = np.diag([0.01, np.radians(1)]) ** 2

map = LandmarkMap(20, workspace=10)

veh = Bicycle()  # error free vehicle
veh.control = RandomPath(workspace=map.workspace)

sensor = RangeBearingSensor(veh, map, covar=W)

map.plot()
ekf = EKF(robot=(veh, None), sensor=(sensor, W), joseph=False, verbose=False)
print(ekf)

ekf.run(T=100)

print(ekf.landmark(8))

ekf.plot_map(ellipse=dict(filled=False, color='g'))
veh.plot_xy('b', label='true path')
plt.legend()
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

ax = plt.gca()
ax.set_xlim(0.86, 0.88)
ax.set_ylim(3.70, 3.72)
rvcprint.rvcprint(subfig='b', interval=(0.005, 0.0025))

# ------------------------------------------------------------------------- #

plt.clf()
ekf.disp_P(ekf.P_est, colorbar=True)

print(np.array([h.innov for h in ekf.history]))
rvcprint.rvcprint(subfig='c')

