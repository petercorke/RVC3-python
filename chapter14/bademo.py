#!/usr/bin/env python3

import rvcprint
import numpy as np
import scipy as sp
from scipy.io import loadmat
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm
import cProfile

from spatialmath import SE3
from bundleadjust import BundleAdjust

def float_formatter(x):
    return f"{x:10.4f}"
np.set_printoptions(linewidth=230, formatter=dict(float=float_formatter))
plt.ion()

# moving camera bundle adjustment problem

ncams = 10  # number of cameras
npts = 110  # number of landmark points
visprob = 0.65  # probability of camera seeing a landmark
pixnoise = 0.5 # standard deviation of Gaussian noise added to camera projections
Tshift = SE3(-0.2, 0, 0)  # horizontal shift of camera at each view

# create a camera
cam = CentralCamera(noise=pixnoise)
print(cam)

# setup a bundle adjustment problem
ba = BundleAdjust(cam)

# create the camera nodes, all at the origin
for i in range(ncams):
    ba.add_view(SE3(), fixed=i == 0)



# create a working volume containing npts random points
# x -3 -> 1
# y -2 -> 2
# z  4 -> 8
# np.random.seed(0)

# P = 2 * 2 * (np.random.uniform(size=(3, npts)) - 0.5) + np.c_[-1, 0 , 6].T

P = loadmat('P.mat')['P']

# create the landmark nodes and keep their handles lh(j)
for j in range(npts):
    ba.add_landmark(P[:,j])

# slide the camera in the x-direciton
T = SE3()
for view in ba.views:
    # project all landmarks for this camera position
    p, visible = cam.project_point(P, pose=T, visibility=True)
    
    # find the subset of points that are visible
    for j, vis in enumerate(visible):
        if vis:
            # add to the problem if visible
            if np.random.uniform() < visprob: # with a probability
                ba.add_projection(view, ba.landmarks[j], p[:, j])

    T = T @ Tshift # shift the camera

# display the problem summary
print(ba)

ba.update_index()
# for c in ba.cameras:
#     print(c.name, c.id, c.index, c.index2)
# for l in ba.landmarks:
#     print(l.name, l.id, l.index, l.index2)

# get the state vector
X = ba.getstate()


# get the initial error
err = ba.errors(X)
print(err)

# display the Hessian
ba.spyH(X)

ba.plot()

plt.show(block=True)

# solve the problem
ba.optimize(X)
Xf = ba.optimize(X)


