#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from spatialmath.base import *
from machinevisiontoolbox.base import *
from numpy.polynomial import Polynomial

y = mvtb_load_matfile('data/peakfit.mat')["y"]
plt.plot(y, "-o", label='discrete data')
k, ypk = findpeaks(y)

plt.grid(True)
plt.xlabel('k')
plt.ylabel('y(k)')

rvcprint.rvcprint(subfig='a')

k = np.arange(0, len(y)+1)
poly = Polynomial.fit(k[6:9], y[6:9], 2)

x = np.linspace(5, 10, 50)
plt.plot(x, poly(x), 'r', label='fitted parabola')

r = poly.deriv(1).roots()
plt.plot(r, poly(r), 'rd', label='estimated maxima')

plt.xlim(5, 10)
plt.ylim(0.8, 1.05)
plt.legend(loc='upper right')
rvcprint.rvcprint(subfig='b')

