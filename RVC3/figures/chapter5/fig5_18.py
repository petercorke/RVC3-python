#!/usr/bin/env python3

from roboticstoolbox.mobile.OccGrid import BinaryOccupancyGrid, OccupancyGrid
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from roboticstoolbox import rtb_load_matfile

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

# make the free space
obstacles = floorplan

obstacles[0,:] = 1
obstacles[-1,:] = 1
obstacles[:,0] = 1
obstacles[:,-1] = 1

og = BinaryOccupancyGrid(obstacles)
# og.plot(cmap='gray')

free = Image(obstacles == 0).astype('uint8')
free.disp()
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='a', grid=False)

# ------------------------------------------------------------------------- #

# skeletonise it
skeleton = free.thin()
skeleton.disp(title=False)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='b', grid=False)

# ------------------------------------------------------------------------- #

# inverse skeleton + obstacle in red

(255-skeleton*255).colorize().choose('red', obstacles).disp()
r, c = skeleton.triplepoint().nonzero()
for x, y in zip(r, c):
    plt.plot(x, y, 'ko', markersize=2)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='c', grid=False)

# ------------------------------------------------------------------------- #

im = free.distance_transform(invert=True).disp(title=False, gamma=0.5)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='d', grid=False)

