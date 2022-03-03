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
T.printline(orient='rpy/yxz')

T = SE3.Rt(T.R, 0.3 * T.t / T.t[0])
print(T)

m2 = m.subset(50)  # short list of matches

ba = BundleAdjust(cam)

view1 = ba.add_view(SE3(), fixed=True, color="blue")
view2 = ba.add_view(SE3(0.3, 0, 0), color="red")

for mk in m2:
    line1 = cam.ray(mk.p1)
    line2 = cam.ray(mk.p2, pose=T)
    P, d = line1.closest_to_line(line2)
    # print(P, d)

    landmark = ba.add_landmark(P)
    ba.add_projection(view1, landmark, mk.p1)
    ba.add_projection(view2, landmark, mk.p2)


print(ba)

X = ba.getstate()

err = ba.errors(X)
print(err)

print(X[6:12])
print(view2.coord)

X, resid= ba.optimize(verbose=False)
print(X[6:12])
print(view2.coord)

# some stats
e = np.sqrt(ba.getresidual(X))
print(np.median(e))
print(np.argmax(e, axis=1))
print(e[0, 34], e[1, 6])
#

view2.pose.printline(orient='rpy/yxz')
ba.setstate(X)
view2.pose.printline(orient='rpy/yxz')

ax = smb.plotvol3([0, 4, 0, 4, 0, 4])
ba.plot(
    text=False, 
    vopt=dict(markersize=3, zorder=20),
    eopt=dict(linewidth=0.2, color='k'), 
    camera=dict(shape='camera', scale=0.5),
    ax=ax
    )
# ax.set_box_aspect
ax.view_init(32, -110)


rvcprint.rvcprint(thicken=None)

