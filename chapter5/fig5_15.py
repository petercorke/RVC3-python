#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from roboticstoolbox import loadmat

house = loadmat('data/house.mat')
floorplan = house['house']
places = house['place']

# make the free space
obs = floorplan

obs[0,:] = 1
obs[-1,:] = 1
obs[:,0] = 1
obs[:,-1] = 1

obstacles = Image(obs > 0)
free = Image(obs == 0)

obstacles.disp(title=False)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='a', grid=False)

# skeletonise it
skeleton = free.thin()
skeleton.disp(title=False)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='b', grid=False)

# inverse skeleton + obstacle in red

(~skeleton).colorize().switch(obstacles, 'red').disp()
r, c = skeleton.triplepoint().nonzero()
for y, x in zip(r, c):
    plt.plot(x, y, 'ko', markersize=2)
plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='c', grid=False)

free.distance_transform().disp(title=False)
rvcprint.rvcprint(subfig='d', grid=False)

