#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import rtb_load_jsonfile, rtb_load_matfile, mobile
import matplotlib.pyplot as plt
import matplotlib as mpl

# show a graph

from pgraph import *

data = rtb_load_jsonfile('data/queensland.json')

g = UGraph()
for name, info in data['places'].items():
    g.add_vertex(name=name, coord=info["utm"]) # add places as vertices
for route in data['routes']:
    g.add_edge(route['start'], route['end'], cost=route['distance']) # add routes as edges

g.plot()
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

# show an occgrid
house = rtb_load_matfile('data/house.mat')
floorplan = house['floorplan']

colors = [(1, 1, 1, 0), (1, 0, 0, 1)]

# ax.set_facecolor((1, 1, 1)) # create white background
cmap = mpl.colors.ListedColormap(colors)

# plt.imshow(floorplan, cmap=cmap)

bug = mobile.Bug2(occgrid=floorplan)
bug.plot()

rvcprint.rvcprint(subfig='b')