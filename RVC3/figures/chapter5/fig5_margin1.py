#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import base


np.random.seed(0)
sites = np.random.uniform(size=(2,9))
base.plot_point(sites, 'k*', markersize=10)

# voronoi(sites(:,1), sites(:,2))

from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(sites.T)
ax = ax=plt.gca()
fig = voronoi_plot_2d(vor, ax=ax, show_points=False)
ax.set_aspect('equal')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
rvcprint.rvcprint()
