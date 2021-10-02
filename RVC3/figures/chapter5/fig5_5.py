#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import *
from spatialmath import base

house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']

places = house['places'];
print(places._fieldnames)



bug = Bug2(occgrid=floorplan)
bug.plot()

p = bug.run(places.br3, places.kitchen, animate=True, pause=0, trail=True, label='path')
print(p.shape)

for place in places._fieldnames:
    base.plot_point(places.__dict__[place], 'b*', text=place)

plt.legend()

rvcprint.rvcprint()
