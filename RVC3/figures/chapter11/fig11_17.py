#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm



castle = Image.Read('castle.png', grey=True, dtype='float')
castle.disp(title=False)

plt.plot([0, castle.width], [360, 360], 'y')
plt.xlim(0, castle.width)
rvcprint.rvcprint(subfig='a')

plt.clf()
p = castle.image[360, :]
plt.plot(p)
plt.xlabel('u (pixels)')
plt.ylabel('Pixel value')
plt.xlim(0, castle.width)
plt.grid(True)
rvcprint.rvcprint(subfig='b')

plt.clf()
plt.plot(p, '-o', markersize=4)
plt.xlim(559, 609)
plt.ylabel('Pixel value')
plt.xlabel('u (pixels)')
plt.grid(True)
rvcprint.rvcprint(subfig='c')

plt.clf()
plt.plot(np.diff(p), '-o', markersize=4)
plt.xlim(559, 609)
plt.xlabel('u (pixels)')
plt.ylabel('Derivative of grey value')
plt.grid(True)
rvcprint.rvcprint(subfig='d')

