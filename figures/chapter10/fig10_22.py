#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath.base.graphics import *

nm = 1e-9

lam = np.arange(400, 701, 5) * nm
macbeth = loadspectrum(lam, 'macbeth')

d65 = loadspectrum(lam, 'D65') * 3e9

N = macbeth.shape[1]
N = 18
XYZ = np.empty((N, 3))
Lab = np.empty((N, 3))
for i in range(N):
    L = macbeth[:,i] * d65
    RGB = np.maximum( cmfrgb(lam, L), 0)
    XYZ[i,:] = colorspace_convert(RGB, 'rgb', 'xyz')
    Lab[i,:] = colorspace_convert(RGB, 'rgb', 'lab')

xy = XYZ[:, :2] / np.tile(np.sum(XYZ, axis=1), (2,1)).T
ab = Lab[:, 1:]

plot_chromaticity_diagram('xy')
plot_point(xy.T, marker='k*', text=' {:d}', textargs=dict(fontsize=8))
plt.grid(True)
rvcprint.rvcprint(subfig='a')

#----------------------------------------------------------------------- #


plt.xlim(0.15, 0.6)
plt.ylim(0.15, 0.5)
plt.grid(True)
rvcprint.rvcprint(subfig='b')

#----------------------------------------------------------------------- #


plt.clf()
plot_chromaticity_diagram('ab')
plot_point(ab.T, marker='k*', text=' {:d}', textargs=dict(fontsize=8))
plt.grid(True)
rvcprint.rvcprint(subfig='c')

#----------------------------------------------------------------------- #

plt.xlim(-50, 50)
plt.ylim(-50, 60)
plt.grid(True)
rvcprint.rvcprint(subfig='d')

# plt.show(block=True)
