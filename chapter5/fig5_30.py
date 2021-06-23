#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## lattice after 7 iter
lp = Lattice('iterations', 8)
lp.plan[]

# A-star search
start = [1 2 pi/2]
goal = [2 -2 0]'
lp.query(start, goal)
lp.plot[]
xaxis(-1,3) yaxis(-3,3)

rvcprint.rvcprint(subfig='a')
pause

lp.plan('cost', [1 10 10])
lp.query(start, goal)
lp.plot[]

xaxis(-1,3) yaxis(-3,3)
rvcprint.rvcprint(subfig='b')

