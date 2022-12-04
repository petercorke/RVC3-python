#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = rtb_loadmat('data/house.mat')
floorplan = house['floorplan']
places = house['places']

dx = DistanceTransformPlanner(floorplan)
dx.plan(places.kitchen)
p = dx.query(places.br3)

dx.plot_3d(p)

ax = plt.gca()
for place in places._fieldnames:
    xy = getattr(places, place)

    z = dx.distancemap[xy[1], xy[0]]
    ax.plot(xy[0], xy[1], z + 10, '*y')
    ax.text3D(xy[0], xy[1], z+ 20, place)
# ht = text(xy[0], xy[1], z+ 20, ['  ' location{1}], 'Color', 'k')
# ht.Units = 'normalized'  # put text on the top
ax.grid(True)

rvcprint.rvcprint()
