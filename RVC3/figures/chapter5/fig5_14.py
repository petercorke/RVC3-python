#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

dx = DistanceTransformPlanner(occgrid=floorplan)
dx.plan(places.kitchen)
dx.plot()
# plt.show(block=True)

p = dx.query(places.br3)
print(p.shape)

plt.clf()
dx.plot(p, background=True)

rvcprint.rvcprint()

# plt.show(block=True)

