#!/usr/bin/env python3

from roboticstoolbox import *
import rvcprint
import numpy as np
import matplotlib.pyplot as plt

house = loadmat('data/house.mat')
floorplan = house['house']
places = house['place']

pmarker = dict(markersize=6, color='y')
dx = DistanceTransformPlanner(floorplan, inflate=5)
dx.plan(places.kitchen)
p = dx.query(places.br3)

dx.plot(p, path_marker=pmarker)
rvcprint.rvcprint(subfig='a');

plt.clf()
dx = DistanceTransformPlanner(floorplan)
dx.plan(places.kitchen)
dx.plot(path=p, path_marker=pmarker, start=places.br3)

rvcprint.rvcprint(subfig='b');
