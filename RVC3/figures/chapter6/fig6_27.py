#!/usr/bin/env python3


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from spatialmath import SE2, SE3, base

pg = PoseGraph('data/killian.g2o.zip', laser=True)
print(pg)
print(pg.graph)

og = OccupancyGrid(workspace=[-100, 250, -100, 250], cellsize=0.1, value=np.int32(0))
pg.scanmap(og, maxrange=40)

og.plot(cmap='gray')

base.plot_box(lrbt=(25, 45, 50, 70), color='k', linewidth=2)
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
og.plot(cmap='gray')
plt.xlim(25, 45)
plt.ylim(50, 70)
rvcprint.rvcprint(subfig='b')


