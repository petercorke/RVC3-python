#!/usr/bin/env python3

from distutils.log import debug
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
# from collections.abc import Iterable
from spatialmath.base import *

x = np.linspace(-10, 60, 200);
plt.plot(x, gauss1d(5, 2**2, x), "r", label=r'$x=\mathcal{N}(\mu=2, \sigma=2)$')

x = np.random.normal(5, 2, size=(1_000_000,));
y = (x + 2)**2 / 4;
h, x = np.histogram(y, bins=200, normed=True)
plt.plot(x[:-1], h, 'b', label=r'$y =(x+2)^2/4$')




ax = plt.gca()

plt.vlines(y.mean(), 0, 0.22, linestyle='--', color='b', label=r'$\bar{y}$')
plt.text(15, 0.05, f'$\sigma={y.std():.1f}$')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('PDF')
plt.xlim(-10, 60)
plt.ylim(0, 0.22)
plt.legend()

rvcprint.rvcprint()

