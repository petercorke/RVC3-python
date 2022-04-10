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
plot_spectral_locus('rg', ax=ax, labels=False)

XYZ = np.array([[1.28, -0.28], [-1.72, 2.70], [-0.74, 0.14]])

for rg in XYZ:
    plt.plot(rg[0], rg[1], 'bs')

for i in range(3):
    start = XYZ[i, :]
    end = XYZ[(i+1)%3, :]
    plt.plot([start[0], end[0]], [start[1], end[1]], 'b')
    plt.text(start[0], start[1], " " + "XYZ"[i])


ax.legend()
ax.set_xlabel('r')
ax.set_ylabel('g')

ax.grid()


# plt.show(block=True)
rvcprint.rvcprint(debug=True)
