#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *
from spatialmath import base, SE2


qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

dubins = DubinsPlanner(curvature=1)
path, status = dubins.query(qs, qg)

ax = base.axes_logic(None, 3)

# dubins.plot(path, twod=False, unwrap=False)

x = path[:, 0]
y = path[:, 1]
th = path[:, 2]
# th = np.unwrap(th)
plt.plot(x, y, th, 'r', linewidth=2)
plt.plot([x[0], x[-1]], [y[0], y[-1]], [th[0], th[-1]], 'b')

start_marker = {'marker': 'o',
                'markeredgecolor': 'b',
                'markerfacecolor': 'y', 
                'markersize': 10,
                }

goal_marker = { 'marker': '*',
                'markeredgecolor': 'b',
                'markerfacecolor': 'y',
                'markersize': 16,
                'zorder': 10,
                }

plt.plot(x[0], y[0], th[0], **start_marker)
plt.plot(x[-1], y[-1], th[-1], **goal_marker)

d = 0.2
for k in np.arange(0, len(x), 5):

    T = SE2(path[k, :])
    p1 = T * [0, d]
    p2 = T * [0, -d]
    plt.plot([p1[0, 0], p2[0, 0]], [p1[1, 0], p2[1, 0]], [th[k], th[k]], 'k', linewidth=2)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel(r'$\theta$')

ax.view_init(27, -78)

rvcprint.rvcprint(subfig='b', thicken=None)

# ------------------------------------------------------------------------- #

#2d version

plt.clf()
plt.plot(x, y, 'r', linewidth=2)
plt.plot([x[0], x[-1]], [y[0], y[-1]], 'b')



start_marker = {'marker': 'o',
                'markeredgecolor': 'b',
                'markerfacecolor': 'y', 
                'markersize': 10,
                }

goal_marker = { 'marker': '*',
                'markeredgecolor': 'b',
                'markerfacecolor': 'y',
                'markersize': 16,
                'zorder': 10,
                }

plt.plot(x[0], y[0], **start_marker)
plt.plot(x[-1], y[-1], **goal_marker)

d = 0.2
for k in np.arange(0, len(x), 5):

    T = SE2(path[k, :])
    p1 = T * [0, d]
    p2 = T * [0, -d]
    plt.plot([p1[0, 0], p2[0, 0]], [p1[1, 0], p2[1, 0]], 'k', linewidth=2)

va = VehiclePolygon(scale=0.5)
va.plot(qs, facecolor='none', edgecolor='k')
va.plot(qg, alpha=0.5)

plt.xlabel('x')
plt.ylabel('y')
rvcprint.rvcprint(subfig='a', thicken=None)