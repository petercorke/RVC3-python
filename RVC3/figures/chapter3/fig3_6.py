#! /usr/bin/env python3

from roboticstoolbox import mstraj
import matplotlib.pyplot as plt
import numpy as np
from spatialmath import SO2
from spatialmath.base import plot_point
from rvcprint import rvcprint
from spatialmath.base import plot_box



# one row per waypoint
vertices = np.array([
    [-1, 1,  1, -1, -1],
    [ 1, 1, -1, -1,  1]
])

sq = SO2(30, unit='deg') * vertices
sq = sq.T

traj = mstraj(sq, qdmax=[2,1], dt=0.2, tacc=0)

plt.plot(traj.q[:,0], traj.q[:,1], markersize=8, linewidth=2, color='r', label='$t_{acc}=0$')

traj2 = mstraj(sq, qdmax=[2, 1], dt=0.2, tacc=2)
plt.plot(traj2.q[:,0], traj2.q[:,1], markersize=8, linewidth=2, color='b', label='$t_{acc}=2$')
plt.gca().set_aspect('equal')
plt.grid(True)
plt.xlabel('$\mathbf{x}$')
plt.ylabel('$\mathbf{y}$')
plot_point(sq[:-1].T, 'ko', text="  {}", label='via point') # , markersize=12, fillcolor='k'
plot_point(sq[-1].T, 'ko', text="    , 4")

plt.legend()

# plt.show(block=True)

rvcprint(subfig='a', thicken=1)

# --------------------------------------------------------------------- #

plt.clf()
plt.plot(traj2.t, traj2.q, '.-', markersize=8, linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('q');
plt.grid(True)

lims = plt.gca().get_ylim()
print(lims)

for info in traj2.info:
    t = info.clock
    if t > 0:
        tf = t + 2
    else:
        tf = t + 1
    plot_box(lrbt=[t, tf, *lims], filled=True, color='black', alpha=0.1, zorder=0)
    #plt.plot([t, t], lims, 'k--', linewidth=1.5)
    
plt.legend(['$\mathbf{x}$', '$\mathbf{y}$'])
plt.ylim(lims)
plt.xlim(0, np.max(traj2.t))
rvcprint(subfig='b', thicken=1)

