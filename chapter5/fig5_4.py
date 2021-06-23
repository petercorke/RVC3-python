#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = loadmat('data/house.mat')
floorplan = house['house']
# plt.imshow(floorplan)

places = house['place']
print(places._fieldnames)

bug = Bug2Planner(floorplan)

p = bug.query(places.br3, places.kitchen, animate=True, trail=True)
print(p.shape)

rvcprint.rvcprint()




