#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *

house = rtb_loadmat('data/house.mat')
floorplan = house['floorplan']

places = house['places'];
print(places._fieldnames)

bug = Bug2(occgrid=floorplan)
bug.plot()

p = bug.run(places.br3, places.kitchen, animate=True, trail=True)
print(p.shape)

rvcprint.rvcprint()
