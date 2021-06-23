#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import spatialmath.base as smb

im = Image.Read('notre-dame.png')

p1 =   np.array([
    [44.1364,  377.0654], 
    [94.0065,  152.7850],
    [537.8506,  163.4019],
    [611.8247,  366.4486]
]).T
im.disp(title=False, grid=True)

smb.plot_poly(p1, filled=True, facecolor='b', alpha=0.4)
smb.plot_poly(p1, 'w', close=True, linewidth=1)
mn = p1.min(axis=1)
mx = p1.max(axis=1)
p2 = np.array([
    [mn[0], mn[0], mx[0], mx[0]],
    [mx[1], mn[1], mn[1], mx[1]]
])
smb.plot_poly(p2, 'k--', close=True, linewidth=2)
smb.plot_point(p1, 'wo')  # on top


rvcprint.rvcprint()

