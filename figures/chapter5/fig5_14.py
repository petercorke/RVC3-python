#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from machinevisiontoolbox import Image
from spatialmath import base

# without obstacles
floorplan = np.zeros((6, 6))
dx0 = DistanceTransformPlanner(occgrid=floorplan, metric='euclidean')
dx0.plan((1,1))

# add obstacles
floorplan[2:5, 3:5] = 1
floorplan[3:5, 2] = 1
# floorplan[2:4, 2:4] = 1

dx = DistanceTransformPlanner(occgrid=floorplan, metric='euclidean')
dx.plan((1,1))

ax = base.plotvol3()

D = dx0.distancemap.copy()
X, Y = np.meshgrid(np.arange(0,6), np.arange(0,6))

from scipy import interpolate

# interpolate distance transform without obstacles
Xi, Yi = np.meshgrid(np.arange(0, 6, 0.5), np.arange(0, 6, 0.5))
interp = interpolate.interp2d(X, Y, dx0.distancemap, kind='linear')
Zi = interp(np.arange(0, 6, 0.5), np.arange(0, 6, 0.5)).reshape(Xi.shape)

# now add the obstacles back in
Zi[4:10, 6:10] = np.nan
Zi[6:10, 4:6] = np.nan

ax.plot_surface(Xi, Yi, Zi)

ax.view_init(37, -151)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('distance from goal')
ax.set_box_aspect((1, 1, 0.7))
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #


p = dx.query((5, 4))
print(p)
dx.plot(p)
ax = plt.gca()
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 5.5)

rvcprint.rvcprint(subfig='b')


