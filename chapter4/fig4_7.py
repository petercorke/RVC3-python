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
dict = runpy.run_path("rvc4_6.py")
g = globals()
for key in ['bd', 'sim', 'L']:
    g[key] = dict[key]

sim.options.animation = False
sim.options.graphics = False

xc = 5
yc = 5
N = 4
radius = 3

ax = base.plotvol2([0, 10], grid=True)
v = Bicycle()
for i in range(N):
    th = (i - 1) * 2 * pi / N
    x0 = np.r_[xc + radius * cos(th), yc + radius * sin(th), th + pi / 2]

    v.plot(x0, size=0.5, color='k')
    bd['vehicle']._x0 = x0  # TODO make this x0 not _x0
    out = sim.run(bd, T=20)

    plt.plot(out.x[:, 0], out.x[:, 1])

base.plot_homline(L, "r--", ax=ax, xlim=np.r_[0, 10], ylim=np.r_[0, 10])


rvcprint.rvcprint()
