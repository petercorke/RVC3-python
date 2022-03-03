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
  [ 44.1364,   94.0065,  537.8506,  611.8247], 
  [377.0654,  152.7850,  163.4019,  366.4486]])

im.disp(title=False, grid=True)

smb.plot_polygon(p1, filled=True, color='y', alpha=0.4, linewidth=2)
mn = p1.min(axis=1)
mx = p1.max(axis=1)
p2 = np.array([
    [mn[0], mn[0], mx[0], mx[0]],
    [mx[1], mn[1], mn[1], mx[1]]
])
smb.plot_polygon(p2, 'k--', close=True, linewidth=2, label='undistorted shape')
smb.plot_point(p1, 'yo', label='distorted shape')  # on top

plt.legend()

rvcprint.rvcprint()

