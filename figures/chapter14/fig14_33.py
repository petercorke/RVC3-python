#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from matplotlib.colors import ListedColormap

import pickle
disparity, similarity, DSI = pickle.load(open('DSI.p', 'rb'))

_, A = Image.DSI_refine(DSI)

Image(A).disp(colorbar=True)


status = np.ones(disparity.shape)
U, V = disparity.meshgrid()
status[np.isnan(disparity.image)] = 5

status[U<=90] = 2
status[similarity.image<0.6] = 3
status[A.image>=-0.1] = 4

cmap = ListedColormap(['lightgreen', 'cyan', 'blue', 'orange', 'red'])
Image(status).disp(ncolors=5, colormap=cmap, colorbar=dict(shrink=0.92, aspect=20*0.92, ticks=[1,2,3,4,5]))
# print(plt.gcf().axes[1].get_yticklabels())
plt.gcf().axes[1].set_yticklabels(['OK', 'no overlap', 'weak match', 'broad peak', 'NaN'])

rvcprint.rvcprint()
