#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *
from spatialmath import SE2, SE3
from spatialmath.base import ICP2d

pg = PoseGraph('data/killian.g2o.zip', laser=True)
print(pg)
print(pg.graph)

p100 = pg.scanxy(100)
p101 = pg.scanxy(101)

plt.plot(p100[0, :], p100[1, :], 'bo', markersize=4, markerfacecolor='none', label='scan 100')
plt.plot(p101[0, :], p101[1, :], 'rx', markersize=4, label='scan 101')
plt.legend(loc='lower right')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(0, 10)
plt.ylim(-3, 2)

rvcprint.rvcprint(subfig='a', debug=False)

# ------------------------------------------------------------------------- #

# import open3d as o3d

# # convert 2d point sets to Open3D point clouds
# pc2580 = o3d.geometry.PointCloud()
# pc2580.points = o3d.utility.Vector3dVector(np.vstack([p100, np.zeros((1, p100.shape[1]))]).T)
# pc2581 = o3d.geometry.PointCloud()
# pc2581.points = o3d.utility.Vector3dVector(np.vstack([p101, np.zeros((1, p101.shape[1]))]).T)

# # Parameters:
# initial_T = SE3(0.5, 0, 0).A # Initial transformation for ICP

# distance = 0.01 # The threshold distance used for searching correspondences (closest points between clouds). I'm setting it to 10 cm.

# # Define the type of registration:
# type = o3d.pipelines.registration.TransformationEstimationPointToPoint(False)
# # "False" means rigid transformation, scale = 1

# # Define the number of iterations (I'll use 100):
# iterations = o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration = 100)

# # Do the registration:
# result = o3d.pipelines.registration.registration_icp(pc2580, pc2581, 
#     distance, initial_T, type, iterations)

# print(result)
# # T = icp( p101, p100, 'verbose' , 'T0', transl2(0.5, 0), 'distthresh', 3)
# # p101t = homtrans(T, p101)

# T = result.transformation
# T = np.delete(T, 2, axis=0)
# T = np.delete(T, 2, axis=1)
# T = SE2(T)

# import pickle

# file = open('scans.p', 'wb')
# pickle.dump(dict(s1=p100, s2=p101), file=file)
# file.close()

# import cv2

# T = cv2.estimateAffine2D(p100.T.astype('float32'), p101.T.astype('float32'), ransacReprojThreshold=0.01, method=cv2.LMEDS)[0]



T = ICP2d(p100, p101)
T = SE2(T)


print(T)
p101t = T * p101

plt.clf()
plt.plot(p100[0, :], p100[1, :], 'bo', markersize=4, markerfacecolor='none', label='scan 100')
plt.plot(p101t[0, :], p101t[1, :], 'rx', markersize=4, label='scan 101 (transformed)')
plt.legend(loc='lower right')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(0, 10)
plt.ylim(-3, 2)

rvcprint.rvcprint(subfig='b')

print(pg.time(2581) - pg.time(2580))
