#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox.mobile import *
from spatialmath import SE2

# EKF SLAM

map = LandmarkMap(20, workspace=10)

V = np.diag([0.02, np.radians(0.5)]) ** 2
W = np.diag([0.01, np.radians(1)]) ** 2
P0 = np.diag([0.05, 0.05, np.radians(5)]) ** 2

robot = Bicycle(covar=V, x0=[3, 6, np.radians(-45)])
robot.control = RandomPath(workspace=map.workspace)

sensor = RangeBearingSensor(robot, map, covar=W, animate=True, range=6,
    angle=[-np.pi/2, np.pi/2], verbose=False)
ekf = EKF(robot=(robot, V), P0=P0, sensor=(sensor, W), verbose=False)
print(ekf)

# map.plot()

# ekf.run(T=40)
# ekf.plot_map(confidence=0.99, ellipse=dict(filled=False, color='g'))

# robot.plot_xy()
# ekf.plot_xy()
# # ekf.plot_map(filled=True, color='g', alpha=0.5)
# plt.legend(loc='lower right')

# # print(ekf.landmark(16))
# # print(ekf.landmark(18))


# rvcprint.rvcprint(debug=True)

ekf.run(T=40)

plt.clf()
map.plot()
robot.plot_xy(color='b', label='true robot path')
plt.legend()
v = VehiclePolygon('car')
v.plot(robot.x0, facecolor='none', edgecolor='k')
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #


# uses singular value decomposition to find the 
# transformation from the target to the source point cloud
# assumes source and target point clounds are ordered such that 
# corresponding points are at the same indices in each array
#
# params:
#   source: numpy array representing source pointcloud
#   target: numpy array representing target pointcloud
# returns:
#   T: transformation between the two point clouds
def align2d(source, target):

    # first find the centroids of both point clouds
    src_centroid = np.mean(source, axis=0)
    trg_centroid = np.mean(target, axis=0)

    # get the point clouds in reference to their centroids
    source_centered = source - src_centroid
    target_centered = target - trg_centroid

    # get cross covariance matrix M
    M = np.dot(target_centered.T,source_centered)

    # get singular value decomposition of the cross covariance matrix
    U,W,V_t = np.linalg.svd(M)

    # get rotation between the two point clouds
    R = np.dot(U,V_t)

    # get the translation (simply the difference between the point clound centroids)
    t = np.expand_dims(trg_centroid,0).T - np.dot(R,np.expand_dims(src_centroid,0).T)

    # assemble translation and rotation into a transformation matrix
    T = np.identity(3)
    T[:2,2] = np.squeeze(t)
    T[:2,:2] = R

    return T




plt.clf()
ekf.plot_xy(color='r', label='estimated path')
ekf.plot_map(confidence=0.99, ellipse=dict(filled=False, color='g'))
v.plot(ekf._x0, facecolor='none', edgecolor='k')
# plt.legend(loc='lower right')

# print(ekf.landmark(16))
# print(ekf.landmark(18))

p = []
q = []

for lm_id in ekf._landmarks.keys():
    p.append(map[lm_id])
    q.append(ekf.landmark_x(lm_id))

p = np.array(p)
q = np.array(q)

# get transform from world to EKF frame
T = align2d(p, q)
T = SE2(T)
print(T)
path = T * robot.x_hist[:, :2].T
plt.plot(path[0, :], path[1, :], 'b--', label='robot path in SLAM frame')

lm = T * map.landmarks
plt.plot(lm[0, :], lm[1, :], 'kx', label='landmark in SLAM frame')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.xlim(-10, 10)
plt.ylim(-15, 5)
plt.gca().set_aspect('equal')

rvcprint.rvcprint(subfig='b')

