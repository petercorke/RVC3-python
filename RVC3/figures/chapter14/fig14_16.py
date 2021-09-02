#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import spatialmath.base as smb


im1 = Image.Read('walls-l.png', reduce=2) #'reduce', 2)
im2 = Image.Read('walls-r.png', reduce=2) #'reduce', 2)

s1 = im1.SIFT()
s2 = im2.SIFT()

m = s1.match(s2)
 
cv.setRNGSeed(0)

F, inliers = CentralCamera.FfromPoints(m.pt1, m.pt2, 
    'ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)

cam = CentralCamera()
cam.disp(im1)

print(inliers.sum())
cam.plot_epiline(F.T, m[inliers][::50].pt2, 'b', linewidth=1)

rvcprint.rvcprint(thicken=None)
