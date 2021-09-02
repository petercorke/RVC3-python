#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *


# Particle filter

V = np.diag([0.02, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, animation='car', workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

map = LandmarkMap(nlandmarks=20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W, plot=True)

Q = np.diag([0.1, 0.1, np.radians(1)]) ** 2
L = np.diag([0.1, 0.1])

pf = ParticleFilter(veh, sensor=sensor, Q=Q, L=L, nparticles=1000)
print(pf)

plt.clf()
pf.run(T=0)
plt.legend(loc='upper right')
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
pf.run(T=1)
plt.legend(loc='upper right')
veh._timer.remove()
rvcprint.rvcprint(subfig='b')

# ------------------------------------------------------------------------- #

plt.clf()
pf.run(T=3)
plt.legend(loc='upper right')
veh._timer.remove()
rvcprint.rvcprint(subfig='c')


