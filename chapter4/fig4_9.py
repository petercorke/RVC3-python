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

# TODO refactor this
dict = runpy.run_path("rvc4_8.py")
g = globals()
for key in ['bd', 'sim', 'total_time', 'path']:
    g[key] = dict[key]

sim.options.animation = False
sim.options.graphics = False

out = sim.run(bd, T=total_time)

ax = base.plotvol2([0, 90], grid=True)
plt.plot(path[:,0], path[:,1], 'r-', linewidth=3, alpha=0.5)
plt.plot(path[:-1, 0], path[:-1, 1], 'ro')
plt.plot(path[-1, 0], path[-1, 1], 'r*')
plt.plot(out.x[:, 0], out.x[:, 1], 'k')



rvcprint.rvcprint()