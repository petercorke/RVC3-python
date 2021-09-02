#!/usr/bin/env python3

import rvcprint
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im1 = Image.Read('eiffel2-1.png', grey=True)
sf2 = Image.Read('eiffel2-2.png', grey=True).SIFT()

m = im1.SIFT().match(sf2)
F, inliers = CentralCamera.points2F(m.pt1, m.pt2, 
    'ransac', ransacReprojThreshold=2, confidence=0.9, maxIters=100)

cam = CentralCamera()
cam.disp(im1)
cam.plot_epiline(F.T, m[inliers][:20].pt2, 'w')
epipole = base.h2e(sp.linalg.null_space(F))
# h2e( null(F))
# cam.hold(true)
cam.plot(epipole, marker='d', markerfacecolor='w', markeredgecolor='k')

rvcprint.rvcprint(debug=True)
