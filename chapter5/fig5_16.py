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

prm.plot()

rvcprint.rvcprint(subfig='a')

prm = PRMPlanner(occgrid=floorplan, seed=0)
prm.plan(npoints=40, dist_thresh=150)
prm.plot()

rvcprint.rvcprint(subfig='b')
