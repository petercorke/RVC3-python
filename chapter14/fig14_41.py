#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
import cv2 as cv
import spatialmath.base as smb

im1 = Image.Read('walls-l.png', reduce=2) #'reduce', 2)
im2 = Image.Read('walls-r.png', reduce=2) #'reduce', 2)

s1 = im1.SIFT()
s2 = im2.SIFT()

m = s1.match(s2)
 
cv.setRNGSeed(0)
F, resid, inliers  = CentralCamera.points2F(m.p1, m.p2, 
    method='ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)
print(resid)

m = m[inliers]
p1 = smb.e2h(m[:10].p1)
p2 = smb.e2h(m[:10].p2)

print(np.diag(p1.T @ F @ p2))

# iphone has 1.5um pixels, double for the image subsampling
cam = CentralCamera(f=4.15e-3, rho=2*1.5e-6)
cam = CentralCamera(f=8.15e-3, rho=2*1.5e-6)

E = cam.E(F)
print(E)

# these give solutions with same R, but different sign of t
# doesn't matter because next we normalize for tx = 0.3
T = cam.decomposeE(E, m[inliers])
T.printline('rpy/yxz')

T = SE3.Rt(T.R, 0.1 * T.t / T.t[0])
print(T)

m2 = m[::20]  # short list of matches

from bundleadjust import BundleAdjust

ba = BundleAdjust(cam)

c1 = ba.add_view(SE3(), fixed=True)
c2 = ba.add_view(T)

for mk in m2:
    line1 = cam.plucker(mk.p1)
    line2 = cam.move(T).plucker(mk.p2)

    P, d = line1.closest_to_line(line2)
    # print(P, d)

    landmark = ba.add_landmark(P)
    ba.add_projection(c1, landmark, mk.p1)
    ba.add_projection(c2, landmark, mk.p2)


print(ba)

X = ba.getstate()

err = ba.errors(X)
print(err)

print(X[6:12])
print(c2.coord)

X = ba.optimize(verbose=True)
print(X[6:12])
print(c2.coord)

# ba.getcamera[1].print('camera')
# baf.getcamera[1].print('camera')

# baf.getlandmark[4]'



# e = sqrt( baf.getresidual[] )

# median( e(:) )
# find( e(1,:) > 1 )
# [mx,k] = max( e(1,:) )

# baf.plot('NodeSize', 4)
# axis([-2 3 -2 1 -0.5 6])
# view(-162, 34)

# rvcprint.rvcprint

