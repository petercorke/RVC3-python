#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

load road
car = Bicycle('steermax', 0.5)
randinit
rrt = RRT(car, road, 'root', [50 22 0], 'npoints', 1000, 'simtime', 4)
# best
# simtime 0.5, 1500, [50 22 0]

rrt.plan[]
rrt.plot[]
drawnow

vg = rrt.graph.closest([40 45 0])
rrt.graph.coord(vg)
rrt.graph.closest([50 22 0])

p = rrt.query([40 45 0], [50 22 0])


rrt.plot(p)

vdim = [20 30]
plot_vehicle(p(1:80:end,:), 'retain', 'box', 'size', vdim, 'fill', 'r', 'alpha', 0.1)
plot_vehicle(p(end,:), 'retain', 'box', 'size', vdim, 'fill', 'r', 'alpha', 0.1)

axis equal
xaxis[-1,99] yaxis[-1,79]
xaxis[0,99] yaxis[0,79]

rvcprint.rvcprint('opengl')

#plot_vehicle(p, 'box', 'size', vdim, 'fill', 'r', 'alpha', 0.1)


