from roboticstoolbox import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3

hershey_font = rtb_load_jsonfile("data/hershey.json")

letter = hershey_font['B']
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

plt.show(block=True)
print(traj.shape[0])
print(traj.shape[0] * 0.02)

Tp = SE3(0.6, 0, 0.7) * SE3(traj) * SE3.OA( [0, 1, 0], [0, 0, -1])

puma = models.DH.Puma560()
sol = puma.ikine_a(Tp, 'lu')

print(np.all(sol.success))

plt.figure()
puma.plot(sol.q)
