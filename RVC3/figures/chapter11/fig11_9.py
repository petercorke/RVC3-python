#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
import numpy as np

church = Image.Read('church.png', grey=True)

def plotfig(lut=None):
    if lut is not None:
        x = np.arange(256, dtype=np.uint8)
        church.LUT(lut).disp(plain=True)
        pos = plt.gca().get_position()
        print(pos)
        ax = plt.gcf().add_axes([pos.x0-0.01, pos.y0-0.01, 0.2, 0.2])
        ax.set_facecolor('xkcd:salmon')
        ax.plot(x, lut, 'b', linewidth=4)
        ax.set_xlim(0, 255)
        ax.set_ylim(-1, 256)
    else:
        church.disp(plain=True)

plotfig()
rvcprint.rvcprint(subfig='a')

# ## threshold
lut = [255 if i > 180 else 0 for i in np.arange(256)]
plotfig(lut)
rvcprint.rvcprint(subfig='b', facecolor=None)


## histo equalization
h = church.hist()
lut = h.ncdf * 255
plotfig(lut)
rvcprint.rvcprint(subfig='c', facecolor=None)

## gamma
lut = 255 * np.linspace(0, 1, 256) ** (1 / 0.45) 
plotfig(lut)
rvcprint.rvcprint(subfig='d', facecolor=None)

## brighten + clip
lut = np.arange(256) + 100
lut = lut.clip(0, 255)
plotfig(lut)
rvcprint.rvcprint(subfig='e', facecolor=None)

## posterize
lut = [64 * ((i + 32) // 64) for i in np.arange(256)]
plotfig(lut)
rvcprint.rvcprint(subfig='f', facecolor=None)
