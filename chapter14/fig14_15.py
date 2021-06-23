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

H, inliers = CentralCamera.HfromPoints(m.pt1, m.pt2, 
    'ransac', ransacReprojThreshold=4, confidence=0.9, maxIters=100)

im1.disp(title=False)

smb.plot_point(m[inliers].pt1, 'b.')
smb.plot_point(m[~inliers].pt1, 'r.')
rvcprint.rvcprint(subfig='a')

im2.disp(title=False)
rvcprint.rvcprint(subfig='b')

