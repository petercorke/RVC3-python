#!/usr/bin/env python3

from RVC3.tools import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

# for seed in range(100):
#     print(seed)
#     prm = PRMPlanner(occgrid=floorplan, seed=seed)
#     prm.plan(npoints=150)

#     path = prm.query(places.br3, places.kitchen)
#     if path is not None:
#         print(seed)
#         break

prm = PRMPlanner(occgrid=floorplan, seed=0)
prm.plan(npoints=50)  # first plan 
prm.plan(npoints=300)  # second plan
path = prm.query(places.br3, places.kitchen)
print(prm)

prm.plot(path, edge=dict(alpha=0.1), vertex=dict(alpha=0.1))


rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

# zoom in on the goal area

ax = plt.gca()
ax.set_xlim(250, 400)
ax.set_ylim(70, 230)
rvcprint.rvcprint(subfig='b', thicken=None)

