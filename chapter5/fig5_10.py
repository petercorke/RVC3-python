#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = loadmat('data/house.mat')
floorplan = house['house']
places = house['place']

dx = DistanceTransformPlanner(floorplan)
dx.plan(places.kitchen)
p = dx.query(places.br3)

dx.plot(p, background=True)

rvcprint.rvcprint()


