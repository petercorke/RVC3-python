#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *


# EKF slam

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, animation='car', workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

map = LandmarkMap(nlandmarks=20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W)
ekf = EKF(robot=(veh, V), P0=P0, sensor=(sensor, W), verbose=True)
print(ekf)


ekf.run(T=40)

veh.plot_xy('b')
ekf.plot_xy('r')
ekf.plot_map(filled=True, color='g')

plt.show(block=True)
