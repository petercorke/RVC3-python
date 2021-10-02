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
lattice.plan(iterations=10)

lattice.plan(iterations=10)
print(lattice.graph)

qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

path, status = lattice.query(qs, qg)

print(path)
print(status)

lattice.plot(path=path)

ax = plt.gca()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-2, 3)
ax.set_ylim(-3, 3)
v.plot(qs, facecolor='none', edgecolor='k')
v.plot(qg)

rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

plt.clf()

lattice = LatticePlanner(costs=[1, 10, 1])

lattice.plan(iterations=10)
print(lattice.graph)

qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

path, status = lattice.query(qs, qg)

print(path)
print(status)

lattice.plot(path=path)

ax = plt.gca()
ax.set_aspect('equal')
ax.grid(True)
ax.set_xlim(-2, 3)
ax.set_ylim(-3, 3)
v.plot(qs, facecolor='none', edgecolor='k')
v.plot(qg)

rvcprint.rvcprint(subfig='b', thicken=None)
