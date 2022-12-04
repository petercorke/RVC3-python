#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
# from collections.abc import Iterable
from spatialmath.base import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

ax = plotvol3()

X, Y = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100));
P = np.diag([1, 2])**2;
Z = gauss2d([0, 0], P, X, Y)

cz = -0.05
ax.plot_surface(X, Y, Z, cmap='viridis_r', cstride=1, rstride=1)
cset = ax.contour(X, Y, Z, zdir='z', offset=cz, cmap='viridis_r')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlim(cz, 0.08)
label = ax.set_zlabel('g(x,y)')
label.set_position((0.1, 0))
ax.view_init(25, -134)

rvcprint.rvcprint()
