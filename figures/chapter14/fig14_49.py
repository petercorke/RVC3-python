#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import spatialmath.base as smb


images = ImageCollection('mosaic/aerial2-*.png', grey=True)
print(images)
composite = Image.Zeros(2_000, 2_000)
composite.paste(images[0], (0, 0))
# composite.disp()

frames = []

for i in range(1, 6):
    f1 = composite.SIFT()

    new = images[i]
    fi = new.SIFT()
    m = f1.match(fi)

    H, _ = m.estimate(CentralCamera.points2H, "ransac", confidence=0.99)
    
    tile, topleft, corners = new.warp_perspective(H, inverse=True, tile=True)
    frames.append(corners)
    composite.paste(tile, topleft, 'blend')

# show the mosaic
composite.disp(grid=True)

# add the outlines
# for frame in frames:
#     print(frame)
#     smb.plot_poly(frame, 'r', close=True)

rvcprint.rvcprint()
