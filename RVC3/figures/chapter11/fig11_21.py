#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm
from spatialmath.base import plot_circle


castle = Image.Read('castle.png', dtype='float', grey=True)

L = Kernel.LoG(2)
lap = castle.convolve(L)
lap.disp(colormap='signed')
plt.grid(True)
rvcprint.rvcprint(subfig='a')

plt.xlim(550, 630)
plt.ylim(390, 310)
# plt.gca().set_aspect(1)
rvcprint.rvcprint(subfig='b')

plt.clf()
p = lap.image[360, 570:601]
plt.plot(np.arange(570, 601), p, '-o', markersize=6)
plt.xlabel('u (pixels)')
plt.ylabel('|Laplacian| at v=360')

plt.gca().axvline(572.1, color='r', linestyle=':')
plt.gca().axvline(594.6, color='r', linestyle=':')

plt.gca().axvline(577.43, color='r', linestyle='--')
plt.gca().axvline(589.27, color='r', linestyle='--')

plt.xlim(570, 600)
plt.grid(True)
rvcprint.rvcprint(subfig='c')

zc = lap.zerocross()
zc.disp(colormap='invert')
plt.xlim(550, 630)
plt.ylim(390, 310)
plt.grid(True)
rvcprint.rvcprint(subfig='d')

