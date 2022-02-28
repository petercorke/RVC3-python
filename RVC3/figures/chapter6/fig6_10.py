#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from matplotlib.ticker import ScalarFormatter

# EKF localization with landmarks

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2


veh = Bicycle(covar=V, workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

print(veh)
# veh.run(10)

Fx = veh.Fx([0, 0, 0], [0.5, 0.1])
print(Fx)

P0 = np.diag([0.005, 0.005, 0.001]) ** 2

map = LandmarkMap(20)
print(map)

sensor = RangeBearingSensor(veh, map, covar=W, animate=True, range=4,
    angle=[-np.pi/2, np.pi/2], verbose=True)
print(sensor)
ekf = EKF(robot=(veh, V), P0=P0, map=map, sensor=(sensor, W))

print(ekf)

ekf.run(T=40)


plt.clf()
t = ekf.get_t()
p = ekf.get_Pnorm()
plt.plot(t, p, 'k')
sf = ScalarFormatter(useOffset=True, useMathText=True)
sf.set_powerlimits((-2, 2))
plt.gca().yaxis.set_major_formatter(sf)
plt.xlabel('Time (s)')
plt.ylabel('$\mathbf{(det P)^{0.5}}$')
plt.grid(True)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

fig, axes = plt.subplots(4)
ekf.plot_error(confidence=0.95, color='k', ax=axes)

# Useful tip from the late creator of matplotlib, John Hunter.

# http://matplotlib.1069221.n5.nabble.com/dynamically-add-subplots-to-figure-td23571.html

# now later you get a new subplot; change the geometry of the existing
# fig = plt.gcf()
# n = len(fig.axes)
# for i in range(n):
#     fig.axes[i].change_geometry(n+1, 1, i+1)
#     fig.axes[i].xaxis.set_ticklabels([])

# # add the new
# noax = fig.add_subplot(n+1, 1, n+1)

lmlog = np.r_[ekf.sensor._landmarklog]
k =  lmlog != -1
axes[3].plot(t[k], lmlog[k], 'bo', markersize=2)
# plot_poly([1:1000 sensor.landmarklog], 'fill', 'b')
plt.ylabel('landmark id')
plt.xlim(0, t[-1])
plt.ylim(-0.5, 22)
plt.grid(True)
plt.xlabel('Time (s)')


rvcprint.rvcprint(subfig='b')

