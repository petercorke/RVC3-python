#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3


movie = VideoFile('traffic_sequence.mp4', grey=True, dtype='float')

sigma = 0.02
for framenum, im in enumerate(movie):
    # plt.imshow(im.image)
    # plt.pause(0.02)

    if framenum == 0:
        background = im
    else:
        d = im - background
        background += d.clip(-sigma, sigma)

    if framenum > 200:
        break

im.disp()
rvcprint.rvcprint(subfig='a')

background.disp()
rvcprint.rvcprint(subfig='b')

(im - background).disp(colormap='signed', colorbar=dict(shrink=0.87, aspect=20*0.87))
(im - background).stats()
rvcprint.rvcprint(subfig='c')


