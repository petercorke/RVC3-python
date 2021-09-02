#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from machinevisiontoolbox import Image
from spatialmath import base

# without obstacles
floorplan = np.zeros((6, 6))
# dx0 = DistanceTransformPlanner(occgrid=floorplan, metric='euclidean')
# dx0.plan((1,1))

# add obstacles
floorplan[2:5, 3:5] = 1
floorplan[3:5, 2] = 1
# floorplan[2:4, 2:4] = 1

dx = DistanceTransformPlanner(occgrid=floorplan, metric='euclidean')
dx.plan((1,1))

# ax = dx.plot_3d()
# dx.plot_bg()
ax = base.plotvol3()
ax.view_init(30, -122)
# ax = base.plotvol3()
ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)

# D = dx0.distancemap.copy()
# print(D)
X, Y = np.meshgrid(np.arange(0,6), np.arange(0,6))
# Xi, Yi = np.meshgrid(np.arange(-0.5, 7), np.arange(-0.5, 7))

# from scipy import interpolate

# interp = interpolate.interp2d(X, Y, D, kind='linear')

# Z = interp(np.arange(-0.5, 7), np.arange(-0.5, 7)).reshape((8,8))
# print(Z)

# put the NaNs back
# for row, col in zip(*np.where(np.isnan(dx.distancemap))):
#     Z[row+1, col+1] = 10 #np.nan
# Z[3,3] = np.nan

# ax.plot_surface(Xi, Yi, Z, cmap='gray', 
# antialiased=False, rstride=1, cstride=1,
# vmin=0, vmax=10,
#                                linewidth=1) 
                               
                               #, antialiased=True)

# cset = ax.contourf(X, Y, dx.distancemap, 100, zdir='z', offset=0.0, cmap='gray')
fc = np.zeros((6, 6, 4))
fc[..., 3] = 1
for row in range(6):
    for col in range(6):
        if np.isnan(dx.distancemap[row, col]):
            fc[row, col, :3] = (1, 0, 0)
        else:
            fc[row, col, :3] = dx.distancemap[row, col] / 10
ax.plot_surface(X, Y, 0*X, facecolors=fc, rstride=1, cstride=1, antialiased=True, shade=False)
path = dx.query((5, 4))

for p in path:
    x = p[0]
    y = p[1]
    z = dx.distancemap[y, x] + 0.4
    plt.plot([x, x], [y, y], [0, z], 'b')
    base.plot_sphere(0.2, centre=(x, y, z), color='b', zorder=20)

# ax.set_box_aspect([1, 1, 1])


# plt.plot(x, y, z, 'ro-', zorder=20)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #


p = dx.query((5, 4))
print(p)
dx.plot(p)

rvcprint.rvcprint(subfig='b')


