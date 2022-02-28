#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *


# Particle filter

V = np.diag([0.02, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, workspace=10)
veh.control = RandomPath(workspace=veh.workspace)
va = VehiclePolygon(facecolor='None', edgecolor='k', scale=1)

map = LandmarkMap(20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W, plot=True)

R = np.diag([0.1, 0.1, np.radians(1)]) ** 2
L = np.diag([0.1, 0.1])

pf = ParticleFilter(veh, sensor=sensor, R=R, L=L, nparticles=1000, animate=True)
print(pf)

plt.clf()
pf.run(T=0)
va.plot(veh.q)

plt.legend(loc='upper right')
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
pf.run(T=1)
va.plot(veh.q)
plt.legend(loc='upper right')
# veh._timer.remove()
rvcprint.rvcprint(subfig='b')

# ------------------------------------------------------------------------- #

plt.clf()
pf.run(T=3)
va.plot(veh.q)

plt.legend(loc='upper right')
# veh._timer.remove()
rvcprint.rvcprint(subfig='c')


