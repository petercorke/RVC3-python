#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

def simpeaks2(DSI, u, v):
    plt.plot(DSI[v, u, :], '-o', markerfacecolor='b', markeredgecolor='b', markersize=6)
    plt.xlim(0, DSI.shape[2])
    plt.ylim(-1, 1)
    plt.grid(True)
    plt.xlabel('Disparity $\mathbf{d - d_{min}}$ (pixels)')
    plt.ylabel('NCC similarity')
    plt.text(2, -0.9, f"pixel at ({u}, {v})", fontsize=11, weight='bold')


L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, similarity, DSI = L.stereo_simple(R, 3, [40, 90])

import pickle
pickle.dump([disparity, similarity, DSI], open('DSI.p', 'wb'))

# good
# 363, 320
plt.figure()
simpeaks2(DSI, 395, 281)
rvcprint.rvcprint(subfig='a')

# multiple
plt.figure()
simpeaks2(DSI, 351, 453)
rvcprint.rvcprint(subfig='b')

# weak
#simpeaks2(DSI,  410, 276)
plt.figure()
simpeaks2(DSI,  356, 17)
rvcprint.rvcprint(subfig='c')

# broad
plt.figure()
simpeaks2(DSI, 543, 173)
rvcprint.rvcprint(subfig='d')

# plt.show(block=True)