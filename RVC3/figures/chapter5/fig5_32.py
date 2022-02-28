#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt

from spatialmath import Polygon2
from roboticstoolbox.mobile import *


# start and goal configuration
qs = (2, 8, -np.pi/2)
qg = (8, 2, -np.pi/2)

# obstacle map
map = PolygonMap(workspace=[0, 10])
map.add([(5, 50), (5, 6), (6, 6), (6, 50)])
# map.add([(5, 0), (6, 0), (6, 4), (5, 4)])
map.add([(5, 4), (5, -50), (6, -50), (6, 4)])

map.plot()

l=3
w=1.5
v0 = Polygon2([(-l/2, w/2), (-l/2, -w/2), (l/2, -w/2), (l/2, w/2)])

vehicle = Bicycle(steer_max=1, L=2, polygon=v0)
print(vehicle.curvature_max)

rrt = RRTPlanner(map=map, vehicle=vehicle, verbose=False, npoints=50, showsamples=True, seed=0)

rrt.plan(goal=qg)
path, status = rrt.query(start=qs)
print(status)

rrt.g.plot(colorcomponents=False, text=False, force2d=True,
    vopt=dict(color='darkblue', marker='o', markersize=10), 
    eopt=dict(color='darkblue', linewidth=3))
rrt.g.highlight_path(status.vertices, color='r')
plt.gca().set_xlim(0, 11)
rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

plt.clf()
map.plot()
rrt.g.plot(colorcomponents=False, text=False, force2d=True,
    vopt=dict(color='darkblue', marker='o', markersize=10), 
    eopt=dict(color='darkblue', linewidth=3))

rrt.plot(path)
plt.gca().set_xlim(0, 11)
rvcprint.rvcprint(subfig='b', thicken=None)


