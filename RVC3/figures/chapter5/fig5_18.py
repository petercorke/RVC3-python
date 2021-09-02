#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *


house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

prm = PRMPlanner(occgrid=floorplan, seed=0)
prm.plan(npoints=50)

prm.plot()
print(prm)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

# reseed the PRN to get a workable solution
# prm = PRMPlanner(occgrid=floorplan, seed=2)
prm.plan(npoints=300)
prm.plot()
print(prm)

rvcprint.rvcprint(subfig='b', thicken=None)
