#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *


# Particle filter

V = np.diag([0.02, np.radians(0.5)]) ** 2
W = np.diag([0.1, np.radians(1)]) ** 2

veh = Bicycle(covar=V, animation=None, workspace=10)
veh.control = RandomPath(workspace=veh.workspace)

map = LandmarkMap(20, workspace=veh.workspace)
sensor = RangeBearingSensor(veh, map, covar=W, plot=True)

R = np.diag([0.1, 0.1, np.radians(1)]) ** 2
L = np.diag([0.1, 0.1])

pf = ParticleFilter(veh, sensor=sensor, R=R, L=L, nparticles=1000, animate=True)
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
plt.xticks(np.arange(0, 20+1, 5))
plt.grid(True)

rvcprint.rvcprint(subfig='b')

