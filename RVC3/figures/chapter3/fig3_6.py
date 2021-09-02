from roboticstoolbox import mstraj
import matplotlib.pyplot as plt
import numpy as np
from spatialmath import SO2
from spatialmath.base import plot_point
from rvcprint import rvcprint



# one row per waypoint
vertices = np.array([
    [-1, 1,  1, -1],
    [ 1, 1, -1, -1]
])

sq = SO2(30, unit='deg') * vertices
sq = sq.T

traj = mstraj(sq[[1, 2, 3, 0],:], qdmax=[2,1], q0=sq[0,:], dt=0.2, tacc=0)

plt.plot(traj.q[:,0], traj.q[:,1], markersize=8, linewidth=2)

traj2 = mstraj(sq[[1, 2, 3, 0],:], qdmax=[2,1], q0=sq[0,:], dt=0.2, tacc=2)
plt.plot(traj2.q[:,0], traj2.q[:,1], markersize=8, linewidth=2)
plt.gca().set_aspect('equal')
plt.grid(True)
plt.xlabel('$\mathbf{q_0}$')
plt.ylabel('$\mathbf{q_1}$')
plot_point(sq.T, 'ko', label="  {}") # , markersize=12, fillcolor='k'

# plt.show(block=True)

rvcprint(subfig='a', thicken=1)

plt.clf()
plt.plot(traj2.t, traj2.q, '.-', markersize=8, linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('q');
plt.grid(True)

lims = plt.gca().get_ylim()
print(lims)

for info in traj2.info:
    t = info.clock
    plt.plot([t, t], lims, 'k--', linewidth=1.5)
    
plt.legend(['$\mathbf{q_0}$', '$\mathbf{q_1}$'])
plt.ylim(lims)
plt.xlim(0, np.max(traj2.t))
rvcprint(subfig='b', thicken=1)

