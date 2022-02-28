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

plt.plot(x, gauss1d(x0, P0), 'b', label='PDF at $k$')
ax = plt.gca()
ax.axvline(x0, 0, 1, color='b', linestyle=':')


u = 2
F = 1
Vhat = 0.5
xp = x0 + u
Pp = F * P0 * F + Vhat

plt.plot(x, gauss1d(xp, Pp), 'r--', label='predicted PDF at $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':')

H = 1
What = 1
K = Pp * H / (H * Pp * H + What)

xs = 5
nu = xs - H * xp

plt.plot(x, gauss1d(xs, What), 'c', label='sensor PDF at $k+1$')
ax.axvline(xs, 0, 1, color='c', linestyle=':')

xp = xp + K * nu
Pp = Pp - K * H * Pp


plt.plot(x, gauss1d(xp, Pp), 'r', label='estimated PDF at $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('PDF')
plt.xlim(0, 8)
plt.ylim(0, 1)
plt.legend(fontsize='xx-small')

rvcprint.rvcprint(subfig='a', thicken=2)

# ------------------------------------------------------------------------- #

plt.clf()

plt.plot(x, gauss1d(x0, P0), 'b', label='PDF at $k$')
ax = plt.gca()
ax.axvline(x0, 0, 1, color='b', linestyle=':')


u = 2
F = 1
Vhat = 0.5
xp = x0 + u
Pp = F * P0 * F + Vhat

plt.plot(x, gauss1d(xp, Pp), 'r--', label='predicted PDF at $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':')

H = 1
What = 0.3
K = Pp * H / (H * Pp * H + What)

xs = 5
nu = xs - H * xp

plt.plot(x, gauss1d(xs, What), 'c', label='sensor PDF at $k+1$')
ax.axvline(xs, 0, 1, color='c', linestyle=':')

xp = xp + K * nu
Pp = Pp - K * H * Pp


plt.plot(x, gauss1d(xp, Pp), 'r', label='estimated PDF at $k+1$')
ax.axvline(xp, 0, 1, color='r', linestyle=':')


plt.grid(True)
plt.xlabel('x')
plt.ylabel('PDF')
plt.xlim(0, 8)
plt.ylim(0, 1)
plt.legend(fontsize='xx-small')

rvcprint.rvcprint(subfig='b', thicken=2)