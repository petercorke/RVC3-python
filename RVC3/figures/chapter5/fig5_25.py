#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *


og = BinaryOccupancyGrid(workspace=[-5, 5, -5, 5], value=False)
og.set([-2, 0, -2, -1], True)
og.set([2, 3, 0, 4], True)
og.set([0, 2, -2, -2], True)

lattice = LatticePlanner(occgrid=og)

lattice.plan(iterations=None)
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
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

rvcprint.rvcprint(thicken=None)