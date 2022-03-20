#!/usr/bin/env python3

from roboticstoolbox import *
import json
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3
import rvcprint

hdict = rtb_load_jsonfile("../../examples/hershey/hershey.json")

mm = 1e-3
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
plt.plot(traj[:,0]/mm, traj[:,1]/mm, traj[:,2]/mm, linewidth=2)
plt.plot(traj[0,0]/mm, traj[0,1]/mm, traj[0,2]/mm, 'k*', markersize=8)
plt.plot(traj[-1,0]/mm, traj[-1,1]/mm, traj[-1,2]/mm, 'ko')

plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
ax.set_zlabel('z (mm)')

rvcprint.rvcprint(thicken=2)
