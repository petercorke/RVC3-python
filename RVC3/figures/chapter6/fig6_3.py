#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
# from collections.abc import Iterable
from spatialmath import base
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

def gauss2d(mu, sigma, X, Y):

    try:
        sx = sigma[0]
        sy = sigma[1]
    except:
        sx = sigma
        sy = sigma

    X0 = X - mu[0]
    Y0 = Y - mu[1]
    return 1 / (2 * np.pi * sx * sy) * np.exp(
        -((X0 / sx) **2 + (Y0 / sy) ** 2) / 2
        )

def uncertainty(sigma, centres, cz, pdfscale=1.0, point=None):
    X, Y = np.meshgrid(np.arange(100), np.arange(100))
    Z = np.zeros(X.shape)
    
    for c in centres:
        Z += gauss2d(c, sigma, X, Y) * pdfscale
    
    ax = base.plotvol3()
    ax.plot_surface(X, Y, Z, cmap='viridis_r', cstride=1, rstride=1)
    cset = ax.contour(X, Y, Z, zdir='z', offset=cz, cmap='viridis_r')
    # ax.plot_wireframe(X, Y, Z)

    if point is not None:
        ax.plot(point[0], point[1], Z[point[1], point[0]], 'ko', markersize=3, zorder=100)
        ax.plot([point[0], point[0]], [point[1], point[1]], [cz, Z[point[1], point[0]]], 'k', zorder=100)
        ax.plot(point[0], point[1], cz, 'ko', markersize=3, zorder=100)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    label = ax.set_zlabel('Prob. density')
    label.set_position((0.1, 0))
    return ax

ax = uncertainty(3, [(30, 40)], cz=-0.015, point=(20,20))
ax.set_zlim(-0.015, 0.02)
sf = ScalarFormatter(useOffset=True, useMathText=True)
sf.set_powerlimits((-2, 2))
ax.zaxis.set_major_formatter(sf)
rvcprint.rvcprint(subfig='a', thicken=None)

# ------------------------------------------------------------------------- #

plt.clf()
ax = uncertainty(20, [(30, 40)], cz=-3e-4, point=(20,20))
ax.set_zlim(-3e-4, 3e-4)
sf = ScalarFormatter(useOffset=True, useMathText=True)
sf.set_powerlimits((-2, 2))
ax.zaxis.set_major_formatter(sf)
rvcprint.rvcprint(subfig='b', thicken=None)

# ------------------------------------------------------------------------- #

plt.clf()
ax = uncertainty(3, [(35, 56), (30, 40), (66, 23), (55, 62)], pdfscale=0.25, cz=-0.015)
ax.set_zlim(-0.015, 0.02)
sf = ScalarFormatter(useOffset=True, useMathText=True)
sf.set_powerlimits((-2, 2))
ax.zaxis.set_major_formatter(sf)
rvcprint.rvcprint(subfig='c')


