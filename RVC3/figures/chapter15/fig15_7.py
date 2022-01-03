#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default(name='')

P = [1, 1, 5]
p0 = camera.project_point(P)
px = camera.project_point(P, pose=SE3(0.1, 0, 0))
(px - p0) / 0.1
(camera.project_point(P, pose=SE3(0, 0, 0.1)) - p0) / 0.1
(camera.project_point(P, pose=SE3.Rx(0.1)) - p0) / 0.1
J = camera.visjac_p([672, 672], 5)


# Tx
camera.flowfield( [1, 0, 0, 0, 0, 0] )
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

# Tz
camera.flowfield( [0, 0, 1, 0, 0, 0] )
rvcprint.rvcprint(subfig='b', facecolor=None)
# ------------------------------------------------------------------------- #

# Rz
camera.flowfield( [0, 0, 0, 0, 0, 1] )
rvcprint.rvcprint(subfig='c', facecolor=None)
# ------------------------------------------------------------------------- #

# Ry
camera.flowfield( [0, 0, 0, 0, 1, 0] )
rvcprint.rvcprint(subfig='d', facecolor=None)
# ------------------------------------------------------------------------- #

# Ry long focal
camera.f = 20e-3
camera.flowfield( [0, 0, 0, 0, 1, 0] )
rvcprint.rvcprint(subfig='e', facecolor=None)
# ------------------------------------------------------------------------- #

# Ry short focal
camera.clf()
camera.f = 4e-3
camera.flowfield( [0, 0, 0, 0, 1, 0] )
rvcprint.rvcprint(subfig='f', facecolor=None)
