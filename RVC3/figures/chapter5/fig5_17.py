#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import *
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import base

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

print(nex0 := ds.nexpand)
path, status = ds.query(places.br3, sensor=sensorfunc, animate=True) #, verbose=True)
print(ds.nexpand - nex0)
ds.plot(path)

base.plot_box(lrbt=[300, 325, 105, 125], filled=True, facecolor='orange', hatch=r'//////\\\\\\')

rvcprint.rvcprint()

# import cProfile
# cProfile.run('ds.plan(places.kitchen)')
