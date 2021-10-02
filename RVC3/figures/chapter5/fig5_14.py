#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from spatialmath import base

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

dx = DistanceTransformPlanner(occgrid=floorplan)
dx.plan(places.kitchen)
# dx.plot()
# plt.show(block=True)

p = dx.query(places.br3)
print(p.shape)

# plt.clf()
dx.plot(p, background=True)

base.plot_circle(15, 'k', centre=(5, 103), linewidth=3)
base.plot_circle(15, 'k', centre=(590, 206), linewidth=3)

plt.gca().autoscale('both')

rvcprint.rvcprint()

# plt.show(block=True)

