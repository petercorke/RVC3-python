#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

import pickle
disparity, similarity, DSI = pickle.load(open('DSI.p', 'rb'))

DSI_flat = DSI.reshape((-1,DSI.shape[2]))

out = []
for i, d in enumerate(np.argmax(DSI, axis=2).ravel()):
    if 0 < d < 49:
        yp = DSI_flat[i, d-1]
        y = DSI_flat[i, d]
        yn = DSI_flat[i, d+1]
        out.append(yp + yn - 2 * y)
    else:
        out.append(np.nan)

A = Image(-np.array(out).reshape(disparity.shape))
A.disp(colorbar=True)


status = np.ones(disparity.shape)
U, V = disparity.meshgrid()
status[U<=90] = 2
status[similarity.image<0.6] = 3
# status[peak.A>=-0.1] = 4
status[np.isnan(disparity.image)] = 5

Image(status).disp(ncolors=5, colorbar=True, colormap='jet')

# idisp(status, 'nogui')
# colormap( colorname({'lightgreen', 'cyan', 'blue', 'orange', 'red'}) )
# nc = 5
# c = colorbar

# c.TicksMode = 'manual'
# c.Ticks = [1:nc]*(nc-1)/nc-(nc-1)/(2*nc)+1
# lab = {}

# c.TickLabels = {'OK', 'no overlap', 'weak pk', 'broad pk', 'NaN'}

# sum(status(:) == 1) / prod(size(status)) * 100


rvcprint.rvcprint(debug=True)
