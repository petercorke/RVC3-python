#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import *
import numpy as np
import matplotlib.pyplot as plt


house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']
places = house['places']

ds = DstarPlanner(occgrid=floorplan)

ds.plan(places.kitchen)

def sensorfunc(pos):
    if pos[0] == 300:
        print('change triggered at', pos)
        changes = []
        for x in range(300, 325):
            for y in range(115,125):
                changes.append((x, y, np.inf))
        return changes

print(nex0 := ds.dstar.nexpand)
p, status = ds.query(places.br3, sensor=sensorfunc, animate=True)
print(ds.dstar.nexpand - nex0)
ds.plot(p)

# dstar.query(places.br3, change=[((300, 300), [300, 325, 115,125], 10)]);
rvcprint.rvcprint()

# import cProfile
# cProfile.run('ds.plan(places.kitchen)')
