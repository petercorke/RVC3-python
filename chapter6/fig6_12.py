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

t = ekf.get_t()
p = ekf.get_P()

plt.clf()
plt.plot(t, p)
plt.yscale('log')
plt.grid(True)
plt.xlim(0, t[-1])
# sf = ScalarFormatter(useOffset=True, useMathText=True)
# sf.set_powerlimits((-2, 2))
# plt.gca().yaxis.set_major_formatter(sf)
plt.xlabel('Time (s)')
plt.ylabel('$(det P)^{0.5}$')
rvcprint.rvcprint(subfig='a')

Pf = ekf.history[-1].P
plt.clf()
ekf.show_P(Pf)


rvcprint.rvcprint(subfig='b')

