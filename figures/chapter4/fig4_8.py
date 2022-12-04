#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from math import pi, sin, cos
from roboticstoolbox import *
from bdsim import *

import runpy

# TODO refactor this
dict = runpy.run_path("models/drivepoint.py")
g = globals()
for key in ['bd', 'sim']:
    g[key] = dict[key]

sim.set_options(animation = False, graphics = False)

xg = np.r_[5, 5]
bd['goal'].value = xg

xc = 5
yc = 5
N = 8
radius = 3

va = VehiclePolygon(scale=0.5, facecolor='None', edgecolor='k')

plt.figure()
for i in range(N):
    th = (i-1) * 2 * pi / N
    x0 = np.r_[xc + radius * cos(th), yc + radius * sin(th), th + pi / 2]

    va.plot(x0)
    bd['vehicle']._x0 = x0  # TODO make this x0 not _x0
    out = sim.run(bd, T=10, dt=0.1)

    # plot_vehicle(x0, "r", "retain")
    plt.plot(out.x[:, 0], out.x[:, 1])

plt.plot(xg[0], xg[1], "*")
plt.gca().set_aspect('equal')
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint()