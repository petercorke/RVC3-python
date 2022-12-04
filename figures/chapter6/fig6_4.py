#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
# from collections.abc import Iterable
from spatialmath import base
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

x = np.linspace(0, 10, 200)

def gauss1d(mu, var):
    sigma = np.sqrt(var)
    print(mu, sigma)

    return 1.0 / np.sqrt(sigma**2 * 2 * np.pi) * np.exp(-(x-mu)**2/2/sigma**2)
x0 = 2
P0 = 0.25

plt.plot(x, gauss1d(x0, P0), 'b', label='PDF at step $k$')
ax = plt.gca()
ax.axvline(x0, 0, 1, color='b', linestyle=':', label='mean at $k$')

u = 2
F = 1
Vhat = 0
xp = x0 + u
Pp = F * P0 * F + Vhat

plt.plot(x, gauss1d(xp, Pp), 'r--', label='predicted PDF at step $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':', label='predicted mean at $k+1$')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('PDF')
plt.xlim(0, 8)
plt.ylim(0, 1)
plt.legend(fontsize='small')

plt.gca().annotate("odometry", xy=(2, 0.3), xytext=(4.1, 0.29), 
    xycoords='data', textcoords='data',
    arrowprops=dict(arrowstyle="<-")
)

rvcprint.rvcprint(subfig='a', thicken=2)

# ------------------------------------------------------------------------- #

plt.clf()
plt.plot(x, gauss1d(x0, P0), 'b', label='PDF at step $k$')
ax = plt.gca()
ax.axvline(x0, 0, 1, color='b', linestyle=':', label='mean at $k$')

Vhat = 0.5
xp = x0 + u
Pp = F * P0 * F + Vhat

plt.plot(x, gauss1d(xp, Pp), 'r--', label='predicted PDF at $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':', label='predicted mean at $k+1$')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('PDF')
plt.xlim(0, 8)
plt.ylim(0, 1)
plt.legend(fontsize='small')

rvcprint.rvcprint(subfig='b', thicken=2)