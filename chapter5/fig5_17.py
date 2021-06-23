#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *


house = loadmat('data/house.mat')
floorplan = house['house']
places = house['place']

prm = PRMPlanner(occgrid=floorplan, seed=0)
prm.plan(npoints=150, dist_thresh=150)

path = prm.query(places.br2, places.kitchen)
print(path)
prm.plot(path, path_marker=dict(color='k', linewidth=2, linestyle='dashed', zorder=10))


rvcprint.rvcprint(thicken=None)

# zoom in on the goal area

# prm.plot(path, path_marker=dict(color='k', linewidth=2, linestyle='dashed', zorder=10))
# ax = plt.gca()
# ax.set_xlim(150, 400)
# ax.set_ylim(175, 375)
# rvcprint.rvcprint(subfig='b', debug=True)

