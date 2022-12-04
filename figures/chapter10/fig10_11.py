#!/usr/bin/env python3

from machinevisiontoolbox.base.color import plot_spectral_locus
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from machinevisiontoolbox import *
import machinevisiontoolbox.base as mvtbase

nm = 1e-9

ax = plt.subplot(1, 1, 1)

# spectral locus
plot_spectral_locus('rg', ax=ax)

# show and label primaries
prim = lambda2rg(cie_primaries())

ax.plot(prim[0, 0], prim[0, 1], marker='o', markeredgecolor='k', markerfacecolor='r', markersize=12, zorder=10)
ax.plot(prim[1, 0], prim[1, 1], marker='o', markeredgecolor='k', markerfacecolor='g', markersize=12, zorder=10)
ax.plot(prim[2, 0], prim[2, 1], marker='o', markeredgecolor='k', markerfacecolor='b', markersize=12, zorder=10)
ax.text(prim[0, 0], prim[0, 1], '  R', fontsize=12)
ax.text(prim[1, 0], prim[1, 1], '  G', fontsize=12)
ax.text(prim[2, 0], prim[2, 1], '  B', fontsize=12)

# RGB space as a yellow triangle
poly = Polygon(prim, closed=True, facecolor='yellow', edgecolor='none', alpha=0.75)
poly.set_color=None
ax.add_patch(poly)

# purple boundary
ax.plot([prim[0, 0], prim[2, 0]], [prim[0, 1], prim[2, 1]], color='purple', linewidth=4)

ax.grid()

ax.set_xlabel('r')
ax.set_ylabel('g')

# plt.show(block=True)
rvcprint.rvcprint(interval=0.5, thicken=None)
