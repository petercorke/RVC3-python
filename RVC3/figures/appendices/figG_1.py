#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
# from collections.abc import Iterable
from spatialmath.base import *


x = np.linspace(-6, 6, 500);
plt.plot(x, gauss1d(0, 1, x), "r", label='$\sigma=1$')
plt.plot(x, gauss1d(0, 2**2, x), "b", label='$\sigma=2$')

plt.xlabel('x');
plt.ylabel('g(x)');
plt.xlim(-6, 6)
ax = plt.gca()

s = 1; g1 = gauss1d(0, 1, s)
plt.plot([-s, s], [g1, g1], 'ko')
plt.hlines(g1, -6, 6, linestyle='--', color='k')

s = 2; g2 = gauss1d(0, 2**2, s)
plt.plot([-s, s], [g2, g2], 'ko')
plt.hlines(g2, -6, 6, linestyle='--', color='k')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('g(x)')
plt.legend()

rvcprint.rvcprint()

