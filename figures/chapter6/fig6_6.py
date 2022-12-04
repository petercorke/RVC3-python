#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from matplotlib.ticker import ScalarFormatter

# EKF dead reckoning
V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([.05, .05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

# odo = veh.step(1, 0.3)
# odo = veh.step(1, 0.3)
print(veh)
# veh.run(10)

Fx = veh.Fx([0, 0, 0], [0.5, 0.1])
print(Fx)

P0 = np.diag([0.005, 0.005, 0.001]) ** 2
ekf = EKF(robot=(veh, V), P0=P0)

ekf.run(T=20)

# from previous fig
p0 = ekf.get_Pnorm()

# redo the sims for different values of V
ekf = EKF(robot=(veh, 2 * V), P0=P0)
ekf.run(T=20)
pb = ekf.get_Pnorm()

ekf = EKF(robot=(veh, 0.5 * V), P0=P0)
ekf.run(T=20)
ps = ekf.get_Pnorm()

t = ekf.get_t()
plt.plot(t, ps, 'r--', label='0.5')
plt.plot(t, p0, 'g', label='1')
plt.plot(t, pb, 'b--', label='2')

plt.legend()

sf = ScalarFormatter(useOffset=True, useMathText=True)
sf.set_powerlimits((-2, 2))
plt.gca().yaxis.set_major_formatter(sf)

plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('$\mathbf{(det P)^{0.5}}$')
plt.xlim(0, 20)

rvcprint.rvcprint()

