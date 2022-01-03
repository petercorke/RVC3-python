#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

walls_l = Image.Read('walls-l.png', reduce=2)
walls_r = Image.Read('walls-r.png', reduce=2)

sL = walls_l.SIFT()
sR = walls_r.SIFT()
matches = sL.match(sR)

F, resid = matches.estimate(CentralCamera.points2F, 
    'ransac', confidence=0.95, seed=0)

# retval, H1, H2 = cv.stereoRectifyUncalibrated(m.pt1[:,inliers], m.pt2[:,inliers], F, L.size)

HL, HR = walls_l.rectify_homographies(matches, F)

print(HL)
print(HR)

walls_l_rect = walls_l.warp_perspective(HL)
walls_r_rect = walls_r.warp_perspective(HR)

disparity = walls_l_rect.stereo_SGBM(walls_r_rect, 7, [180, 530], (50, 2))
disparity.disp(grid=True, colorbar=dict(shrink=0.92, aspect=20*0.92, label='Disparity (pixels)'))
plt.xlim(200, disparity.width)

rvcprint.rvcprint()
