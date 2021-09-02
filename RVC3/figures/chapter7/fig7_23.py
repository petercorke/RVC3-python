#!/usr/bin/env python3

from roboticstoolbox import *
import json
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3
import rvcprint

with (open("writing/hershey.json", "r")) as file:
    hdict = json.load(file)

letter = hdict['B']
print(letter)
lift = 0.1
scale = 0.25
via = np.empty((0, 3))
for stroke in letter['strokes']:
    xyz = np.pad(np.array(stroke) * scale, ((0, 0), (0, 1)))
    via = np.vstack((via, xyz, np.r_[xyz[-1,:2], lift]))

traj = mstraj(via, dt=0.02, qdmax=[0.5, 0.5, 0.5], q0=[0, 0, lift], tacc=0.2).q

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(traj[:,0], traj[:,1], traj[:,2], linewidth=2)
plt.plot(traj[0,0], traj[0,1], traj[0,2], 'k*', markersize=8)
plt.plot(traj[-1,0], traj[-1,1], traj[-1,2], 'ko')

plt.xlabel('x')
plt.ylabel('y')
ax.set_zlabel('z')

rvcprint.rvcprint(thicken=2, interval=0.05)
