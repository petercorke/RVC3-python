#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *


qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

dubins = DubinsPlanner(curvature=1)
path, status = dubins.query(qs, qg)

dubins.plot(path)
rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

rs = ReedsSheppPlanner(curvature=1)
path, status = rs.query(qs, qg)

plt.clf()
rs.plot(path, direction=status.direction)
rvcprint.rvcprint(subfig='b', thicken=None)