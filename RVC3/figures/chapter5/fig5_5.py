#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from spatialmath import base

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']

places = house['places'];

bug = Bug2(occgrid=floorplan)
bug.plot()

p = bug.run(places.br3, places.kitchen, animate=True, pause=0, trail=True, label='path')
print(p.shape)

for place, pos in places.items():
    base.plot_point(pos, 'b*', text=place)

plt.legend(loc='upper left')

rvcprint.rvcprint()
