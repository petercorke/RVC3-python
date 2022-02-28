#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *

lattice = LatticePlanner()


## lattice after 2 iter
lattice.plan(iterations=2)

lattice.plot(configspace=True)

ax = plt.gca()
# ax.set_aspect('equal')
ax.grid(True)
ax.view_init(9, -46)
ax.set_xlim(-1, 3)
ax.set_ylim(-3, 3)

rvcprint.rvcprint(thicken=None, interval=1)

