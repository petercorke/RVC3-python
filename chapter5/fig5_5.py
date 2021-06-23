#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import loadmat, path_to_datafile, mobile
import matplotlib.pyplot as plt
import matplotlib as mpl


from pgraph import *
import json
with open(path_to_datafile('data/queensland.json'), 'r') as f:
    data = json.loads(f.read())
g = UGraph()
for name, info in data['places'].items():
    g.add_vertex(name=name, coord=info["utm"]) # add places as vertices
for route in data['routes']:
    g.add_edge(route['start'], route['end'], cost=route['distance']) # add routes as edges

g.plot()
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint(subfig='a')


house = loadmat('data/house.mat')
floorplan = house['house']

colors = [(1, 1, 1, 0), (1, 0, 0, 1)]

# ax.set_facecolor((1, 1, 1)) # create white background
cmap = mpl.colors.ListedColormap(colors)

# plt.imshow(floorplan, cmap=cmap)

bug = mobile.Bug2Planner(floorplan)
bug.plot()

rvcprint.rvcprint(subfig='b')