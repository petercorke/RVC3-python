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

im1.disp(title=False)


H, inliers = m.estimate(CentralCamera.points2H, 
    'ransac', confidence=0.9, seed=0)
smb.plot_point(m.inliers.p1, 'r.')

m = m.outliers
H, inliers = m.estimate(CentralCamera.points2H, 
    'ransac', confidence=0.9, seed=0)
smb.plot_point(m.inliers.p1, 'y.')

m = m.outliers
H, inliers = m.estimate(CentralCamera.points2H, 
    'ransac', confidence=0.9, seed=0)
smb.plot_point(m.inliers.p1, 'b.')
plt.legend(['first plane', 'second plane', 'third plane'])

rvcprint.rvcprint(subfig='a')
#----------------------------------------------------------------------- #

im2.disp(title=False)
rvcprint.rvcprint(subfig='b')

