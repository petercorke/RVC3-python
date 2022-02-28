#!/usr/bin/env python3

import rvcprint
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import spatialmath.base as smb

im1 = Image.Read('eiffel-1.png')
sf2 = Image.Read('eiffel-2.png').SIFT()

m = im1.SIFT().match(sf2)
# F, inliers, resid = CentralCamera.points2F(m.p1, m.p2, 
#     'ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)

F, resid = m.estimate(CentralCamera.points2F, 
    method='ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)

a = m.inliers
print(len(a))
b = m.outliers
print(len(b))

cam = CentralCamera()
cam.disp(im1)
# cam.plot_epiline(F.T, m.inliers.subset(20).p2, 'k')
epipole = smb.h2e(sp.linalg.null_space(F))
# h2e( null(F))
# cam.hold(true)
cam.plot_point(epipole, 'wd')

rvcprint.rvcprint(debug=True)
