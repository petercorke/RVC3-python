#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *

lattice = LatticePlanner()

v = VehiclePolygon('car', scale=0.5)

## lattice after 1 iter
lattice.plan(iterations=1)

plt.clf()
lattice.plot()

ax = plt.gca()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-1, 3)
ax.set_ylim(-3, 3)
v.plot((0, 0, 0), facecolor='none', edgecolor='k')

rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #


## lattice after 2 iter
lattice.plan(iterations=2)
lattice.plot()

ax = plt.gca()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-1, 3)
ax.set_ylim(-3, 3)
v.plot((0, 0, 0), facecolor='none', edgecolor='k')

rvcprint.rvcprint(subfig='b', thicken=None)

# ------------------------------------------------------------------------- #


# ## lattice after 7 iter
lattice.plan(iterations=7)
lattice.plot()

ax = plt.gca()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-1, 3)
ax.set_ylim(-3, 3)
v.plot((0, 0, 0), facecolor='none', edgecolor='k')

rvcprint.rvcprint(subfig='c', thicken=None)