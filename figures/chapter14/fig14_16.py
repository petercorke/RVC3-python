#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import spatialmath.base as smb
import cv2 as cv


im1 = Image.Read('walls-l.png', reduce=2)
im2 = Image.Read('walls-r.png', reduce=2)

s1 = im1.SIFT()
s2 = im2.SIFT()

m = s1.match(s2)
 
cv.setRNGSeed(0)

F, resid, inliers = CentralCamera.points2F(m.p1, m.p2, 
    method='ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)

cam = CentralCamera()
cam.disp(Image(im1.to_float()*0.5))

print(inliers.sum())
cam.plot_epiline(F.T, m[inliers][::50].p2, 'y', linewidth=1)

rvcprint.rvcprint(thicken=None)
