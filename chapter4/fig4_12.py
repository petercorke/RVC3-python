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
dict = runpy.run_path("rvc4_11.py")
g = globals()
for key in ['bd', 'sim']:
    g[key] = dict[key]

sim.options.animation = False
sim.options.graphics = False

xg = np.r_[5, 5, pi / 2]
bd['goalpos'].value = np.r_[xg[:2], 0]
bd['goalheading'].value = xg[2]

xc = 5
yc = 5
N = 8
radius = 4

v = Bicycle()

for i in range(N):
    th = (i-1) * 2 * pi / N
    x0 = np.r_[xc + radius * cos(th), yc + radius * sin(th), 0]

    v.plot(x0, size=0.5, color='k')
    bd['vehicle']._x0 = x0  # TODO make this x0 not _x0
    out = sim.run(bd, T=10)

    # plot_vehicle(x0, "r", "retain")
    plt.plot(out.x[:, 0], out.x[:, 1])

plt.plot(xg[0], xg[1], "*")
plt.gca().set_aspect('equal')
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint()
