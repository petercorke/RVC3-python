#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


sf1 = Image.Read('eiffel2-1.png').SIFT()
sf2 = Image.Read('eiffel2-2.png').SIFT()
m = sf1.match(sf2)
print(m[:5])



cv.setRNGSeed(0)

    # def FfromPoints(cls,
    #                 P1,
    #                 P2,
    #                 method,
    #                 ransacThresh,
    #                 confidence,
    #                 maxiters):


F, inliers = CentralCamera.FfromPoints(m.pt1.T, m.pt2.T, 
    'ransac', ransacReprojThreshold=1, confidence=0.9, maxIters=100)

print(F)

m[inliers].plot('g')
# idisp({im1, im2} , 'nogui', 'dark')
# m.inlier.subset[99].plot('g')
# rvcprint.rvcprint(subfig='a', 'svg')

# idisp({im1, im2} , 'nogui', 'dark')
m[~inliers].plot('r')

# plt.figure()
# im1 = Image.Read('eiffel2-1.png', grey=True)
# im2 = Image.Read('eiffel2-2.png', grey=True)
# Image.Tile([im2, im2]).disp()
# rvcprint.rvcprint(subfig='b', 'svg')
# rvcprint.rvcprint(thicken=None)

plt.show(block=True)