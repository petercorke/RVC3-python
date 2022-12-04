#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from machinevisiontoolbox import Image


floorplan = np.zeros((5, 5))
floorplan[2,1] = 1

Image(floorplan).disp(black=0.3, )
plt.xlabel('x')
plt.ylabel('y')
plt.gca().invert_yaxis()
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

goalmarker = {'marker': ''}
floorplan[2,1] = 0
dx = DistanceTransformPlanner(occgrid=floorplan, metric='euclidean')
dx.plan((1,2))
dx.plot(goal_marker=goalmarker)
ax = plt.gca()
ax.grid(False)
for i in range(floorplan.shape[0]):
    for j in range(floorplan.shape[1]):
        ax.text(x=j, y=i,s=np.round(dx.distancemap[i, j], 2), va='center', ha='center', size='xx-large', color='r')
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.5)

rvcprint.rvcprint(subfig='b')

# ------------------------------------------------------------------------- #

plt.clf()

dx = DistanceTransformPlanner(occgrid=floorplan, metric='manhattan')
dx.plan((1,2))
dx.plot(goal_marker=goalmarker)
ax = plt.gca()
ax.grid(False)
for i in range(floorplan.shape[0]):
    for j in range(floorplan.shape[1]):
        ax.text(x=j, y=i,s=np.round(dx.distancemap[i, j], 2), va='center', ha='center', size='xx-large', color='r')
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-0.5, 4.5)

rvcprint.rvcprint(subfig='c')
