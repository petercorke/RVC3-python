#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *


# Particle filter

V = np.diag([0.02, np.radians(0.5)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, animation=None, workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

map = LandmarkMap(nlandmarks=20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W, plot=True)

Q = np.diag([0.1, 0.1, np.radians(1)]) ** 2
L = np.diag([0.1, 0.1])

pf = ParticleFilter(veh, sensor=sensor, Q=Q, L=L, nparticles=1000)
print(pf)

pf.run(T=20)

plt.clf()
map.plot()
veh.plot_xy('b', label='ground truth')
pf.plot_xy('r', label='particle filter mean')
plt.legend(loc='upper left')

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
t = pf.get_t()
std = pf.get_std()
plt.plot(t, std[:,0], label='x')
plt.plot(t, std[:,1], label='y')
plt.plot(t, 10 * std[:,2], label=r'$\theta$ (x 10)')
plt.legend()
plt.xlabel('Time step')
plt.ylabel('standard deviation')
plt.grid(True)

rvcprint.rvcprint(subfig='b')

