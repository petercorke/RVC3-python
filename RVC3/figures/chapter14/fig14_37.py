#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import cv2 as cv

L = Image.Read('walls-l.png', grey=True, reduce=2)
R = Image.Read('walls-r.png', grey=True, reduce=2)

sL = L.SIFT()
sR = R.SIFT()
m = sL.match(sR)

cv.setRNGSeed(0)

F, resid, inliers = CentralCamera.points2F(m.pt1, m.pt2, 
    'ransac', ransacReprojThreshold=1, confidence=0.99, maxIters=100)

print(len(m), resid, np.sum(inliers))

retval, H1, H2 = cv.stereoRectifyUncalibrated(m.pt1[:,inliers], m.pt2[:,inliers], F, L.size)

print(H1)
print(H2)

Lr = L.warpPerspective(H1)
Rr = R.warpPerspective(H2)

# Lr.stdisp(Rr)

Image.hcat(Lr, Rr)[0].disp()


rvcprint.rvcprint(debug=True)
