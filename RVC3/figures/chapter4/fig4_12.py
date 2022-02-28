#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from math import pi, sin, cos
from roboticstoolbox import *
from bdsim import *
from spatialmath import base

import runpy

# pure pursuit example


# TODO refactor this
dict = runpy.run_path("models/drivepursuit.py")
g = globals()
for key in ['bd', 'sim', 'total_time', 'path']:
    g[key] = dict[key]

sim.set_options(animation = False, graphics = False)

out = sim.run(bd, T=total_time)

ax = base.plotvol2([-5, 90], grid=True)
plt.plot(path[:, 0], path[:, 1], 'ro', label='waypoint')
plt.plot(path[:,0], path[:,1], 'r-', linewidth=3, alpha=0.5, label='desired path')
plt.plot(out.x[:, 0], out.x[:, 1], 'k', label='actual path')
plt.legend()

v = VehiclePolygon('car', scale=8, facecolor='none', edgecolor='k')
v.plot([2, 2, 0])

rvcprint.rvcprint()