#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from spatialmath import SE2, SE3

pg = PoseGraph('data/killian.g2o.zip', laser=True)
print(pg)
print(pg.graph)

p2580 = pg.scanxy(2580)
p2581 = pg.scanxy(2581)

plt.plot(p2580[0, :], p2580[1, :], 'bo', markersize=4, label='scan 2580')
plt.plot(p2581[0, :], p2581[1, :], 'ro', markersize=4, label='scan 2581')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(0, 10)
plt.ylim(-3, 2)

rvcprint.rvcprint(subfig='a')

import open3d as o3d

# convert 2d point sets to Open3D point clouds
pc2580 = o3d.geometry.PointCloud()
pc2580.points = o3d.utility.Vector3dVector(np.vstack([p2580, np.zeros((1, p2580.shape[1]))]).T)
pc2581 = o3d.geometry.PointCloud()
pc2581.points = o3d.utility.Vector3dVector(np.vstack([p2581, np.zeros((1, p2581.shape[1]))]).T)

# Parameters:
initial_T = SE3(0.5, 0, 0).A # Initial transformation for ICP

distance = 0.01 # The threshold distance used for searching correspondences (closest points between clouds). I'm setting it to 10 cm.

# Define the type of registration:
type = o3d.pipelines.registration.TransformationEstimationPointToPoint(False)
# "False" means rigid transformation, scale = 1

# Define the number of iterations (I'll use 100):
iterations = o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration = 100)

# Do the registration:
result = o3d.pipelines.registration.registration_icp(pc2580, pc2581, 
    distance, initial_T, type, iterations)

print(result)
# T = icp( p2581, p2580, 'verbose' , 'T0', transl2(0.5, 0), 'distthresh', 3)
# p2581t = homtrans(T, p2581)

T = result.transformation
T = np.delete(T, 2, axis=0)
T = np.delete(T, 2, axis=1)
T = SE2(T)
print(T)
p2581t = T * p2581

plt.clf()
plt.plot(p2580[0, :], p2580[1, :], 'bo', markersize=4, label='scan 2580')
plt.plot(p2581t[0, :], p2581t[1, :], 'ro', markersize=4, label='scan 2581')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(0, 10)
plt.ylim(-3, 2)

rvcprint.rvcprint(subfig='b')

print(pg.time(2581) - pg.time(2580))
