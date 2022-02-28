#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import rtb_path_to_datafile, mobile
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import json
import os
import numpy as np

with open(rtb_path_to_datafile('data/queensland.json'), 'r') as f:
    data = json.loads(f.read())

g = UGraph()
for name, info in data['places'].items():
    g.add_vertex(name=name, coord=info["utm"]) # add places as vertices
for route in data['routes']:
    g.add_edge(route['start'], route['end'], cost=route['distance']) # add routes as edges

path, *_ = g.path_Astar('Hughenden', 'Brisbane')

plt.clf()
g.plot()
g.highlight_path(path)
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

# minimum time
g = UGraph()
for name, info in data['places'].items():
    g.add_vertex(name=name, coord=info["utm"]) # add places as vertices
for route in data['routes']:
    g.add_edge(route['start'], route['end'], cost=route['distance'] / route['speed']) # add routes as edges
g.heuristic = lambda x: np.linalg.norm(x) / 100

path, *_ = g.path_Astar('Hughenden', 'Brisbane')

plt.clf()
g.plot()
g.highlight_path(path)
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint(subfig='b', thicken=None)
