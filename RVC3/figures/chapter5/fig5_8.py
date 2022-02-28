#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import rtb_path_to_datafile, mobile
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import json

with open(rtb_path_to_datafile('data/queensland.json'), 'r') as f:
    data = json.loads(f.read())
g = UGraph()
for name, info in data['places'].items():
    g.add_vertex(name=name, coord=info["utm"]) # add places as vertices
for route in data['routes']:
    g.add_edge(route['start'], route['end'], cost=route['distance']) # add routes as edges

g.plot()
plt.xlabel('x')
plt.ylabel('y')

path, *_ = g.path_BFS('Hughenden', 'Brisbane')
g.highlight_path(path)

rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

plt.clf()
g.plot()
plt.xlabel('x')
plt.ylabel('y')

path, *_ = g.path_UCS('Hughenden', 'Brisbane')
g.highlight_path(path)

rvcprint.rvcprint(subfig='b', thicken=None)
