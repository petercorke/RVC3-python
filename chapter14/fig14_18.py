#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
import spatialmath.base as smb

import spatialmath.base as smb


im1 = Image.Read('walls-l.png', reduce=2) #'reduce', 2)
im2 = Image.Read('walls-r.png', reduce=2) #'reduce', 2)

s1 = im1.SIFT()
s2 = im2.SIFT()

m = s1.match(s2)
 
cv.setRNGSeed(0)
F, inliers, resid = CentralCamera.FfromPoints(m.pt1, m.pt2, residual=True,
    method='ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)
print(resid)

m = m[inliers]
p1 = smb.e2h(m[:10].pt1)
p2 = smb.e2h(m[:10].pt2)

print(np.diag(p1.T @ F @ p2))

# iphone has 1.5um pixels, double for the image subsampling
cam = CentralCamera(f=4.15e-3, rho=2*1.5e-6)
cam.disp(im1.grey(), darken=True)
# im1 = imono(im1)

E = cam.E(F)
print(E)

# these give solutions with same R, but different sign of t
# doesn't matter because next we normalize for tx = 0.3
T = cam.invE(E, m[inliers])
T.printline('rpy/yxz')
T = cam.invE(E, np.r_[0, 0, 10])
T.printline('rpy/yxz')

T = SE3.Rt(T.R, 0.3 * T.t / T.t[0])
print(T)

lines1 = cam.plucker(m[0].p1)
print(lines1)
lines2 = cam.move(T).plucker(m[0].p2)
print(lines2)

z = lines1.closest_to_line(lines2)
print(z)


m2 = m[::20]  # short list of matches


lines1 = cam.plucker(m2.p1)
lines2 = cam.move(T).plucker(m2.p2)

P1, d = lines1.closest_to_line(lines2)
# P'
# e
# N = 100
# m2 = m.inlier.subset(N)
# r1 = cam.ray( m2.p1 )
# r2 = cam.move(T).ray( m2.p2 )
# [P,e] = r1.intersect(r2)
# z = P(3,:)

# idisp(im1*0.7, 'nogui')
# for i in range(len(m2)):
#     smb.plot_point(m2[i].pt1, 'y+', text=f" {P1[2, i]:.1f}", color='y',
#         textargs=dict(fontsize=8))


smb.plot_point(m2.pt1, 'y+', text=f" {1:.1f}", textdata=(P1[2, :],),
    color='y', textargs=dict(fontsize=8))

# plot_point(m2.pt1, 'y+', text=" {0:.1f}", textargs=(P1[2, :]), color='y')


rvcprint.rvcprint()
