#!/usr/bin/en
import math
from roboticstoolbox.mobile.OccGrid import PolygonMap
import rvcprint
from roboticstoolbox import *
import numpy as np
import matplotlib.pyplot as plt

from spatialmath import Polygon2, SE2, base
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

a = VehicleIcon('piano', scale=3)
vehicle = Bicycle(steer_max=1, l=2, polygon=v0)

a.plot(qs)
a.plot(qg)
a.plot([5.5, 5, 0])

plt.text(2.8, 8, 'start', fontsize=12)
plt.text(8.8, 2, 'goal', fontsize=12)

base.plot_circle(np.linalg.norm([l/2, w/2]), 'k:', centre=(5.5, 5))

base.plot_circle(np.linalg.norm([l/2, w/2]), centre=(5.5, 4), filled=True, color='r', alpha=0.2, zorder=10)
base.plot_circle(np.linalg.norm([l/2, w/2]), centre=(5.5, 6), filled=True, color='r', alpha=0.2, zorder=10)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
map.plot()

rrt = RRTPlanner(map=map, vehicle=vehicle, verbose=False, npoints=50, showsamples=True, seed=0)

for i in range(10):
    q = rrt.qrandom()
    collision = map.collision(vehicle.polygon(q))
    a.plot(q, alpha=0.8, color='r' if collision else 'g')

rvcprint.rvcprint(subfig='b', thicken=None)

