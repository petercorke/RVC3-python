#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from machinevisiontoolbox import *

nm = 1e-9

gcc = lambda2rg(500 * nm).flatten()
wcc = tristim2cc(np.r_[1, 1, 1])

ax = plt.subplot(1,1,1)

# show locus
ax = plt.subplot(1, 1, 1)
λ = np.arange(470, 550, 10)
λ = np.hstack((λ, np.arange(560, 590, 20)))
plot_spectral_locus('rg', ax=ax, lambda_ticks=λ)

# show and label primaries
prim = lambda2rg(np.r_[600, 555, 450] * nm)
poly = Polygon(prim, closed=True, facecolor='yellow', edgecolor='none', alpha=0.75)
ax.add_patch(poly)

ax.plot(prim[0, 0], prim[0, 1], marker='o', markeredgecolor='k', markerfacecolor='r', markersize=12)
ax.plot(prim[1, 0], prim[1, 1], marker='o', markeredgecolor='k', markerfacecolor='g', markersize=12)
ax.plot(prim[2, 0], prim[2, 1], marker='o', markeredgecolor='k', markerfacecolor='b', markersize=12)
ax.text(prim[0, 0], prim[0, 1], "  R'", fontsize=12)
ax.text(prim[1, 0], prim[1, 1], "  G'", fontsize=12)
ax.text(prim[2, 0], prim[2, 1] - 0.06, "  B'", fontsize=12)

# draw line from desired green to white
ax.plot((gcc[0], wcc[0]), (gcc[1], wcc[1]), 'g', label='saturated greens')
ax.plot(gcc[0], gcc[1], 'g', marker='x', linestyle="None", markersize=10, markeredgecolor='g', label='spectral green')
ax.plot(wcc[0], wcc[1], 'w', marker='o', markeredgecolor='k', label='equal energy white')

green = cmfrgb(500e-9)
w = -np.min(green)
white = np.r_[w, w, w]

feasible_green = green + white
fgcc = tristim2cc(feasible_green)
print(fgcc)
ax.plot(fgcc[0], fgcc[1], 'g', marker='s', linestyle="None", markeredgecolor='k', label='feasible green')

# gamut boundary
ax.plot(0.1229, 0.4885, 'g', marker='o', linestyle="None", markeredgecolor='k', label='displayable green')
ax.legend()
ax.set_xlabel('r')
ax.set_ylabel('g')

ax.grid()


# plt.show(block=True)
rvcprint.rvcprint()
