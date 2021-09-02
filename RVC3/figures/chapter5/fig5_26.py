#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *
from scipy.io import loadmat

mprim = loadmat('mprim.mat')
local = mprim['local'][0]

# local is (80) array of structs with elements:
#   primID, startangle_c, endpose_c, poses

markeropt = {'markersize': 4, 'color': 'b'};
lineopt = {'linewidth': 0.2, 'color': [0.5, 0.5, 0.5]}
        

for i in range(len(local)):
    ep = local[i]['endpose_c']
    if ep[0, 1] >= 0:
        plt.plot(local[i]['poses'][-1, 1], local[i]['poses'][-1, 0], 'bo', **markeropt);
        plt.plot(local[i]['poses'][:, 1], local[i]['poses'][:, 0], **lineopt)

plt.plot(0, 0, 'ko', markerfacecolor='k', markersize=8)

plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint(thicken=None)

