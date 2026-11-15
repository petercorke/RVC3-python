#!/usr/bin/env python3

from roboticstoolbox import *
from RVC3.tools import rvcprint
import numpy as np
import matplotlib.pyplot as plt

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

dx = DistanceTransformPlanner(floorplan, inflate=5)
dx.plan(places.kitchen)
p = dx.query(places.br3)

dx.plot(p, inflated=True)
rvcprint.rvcprint()

# plt.clf()
# dx = DistanceTransformPlanner(floorplan)
# dx.plan(places.kitchen)
# dx.plot(path=p, start=places.br3)

# rvcprint.rvcprint(subfig='b');
