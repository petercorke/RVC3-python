#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath.base import plot_box
from matplotlib import cm

im = np.full((5,5), 0, dtype='uint8')

canvas = np.full((7, 55), 128, dtype='uint8')
canvas[1:6, 1:6] = im
count = 2
for v in range(1, 4):
    for u in range(1, 4):
        W = im[v-1:v+2, u-1:u+2]

        k = count * 5
        canvas[2:5, k:k+3] = W
        count += 1

Image(canvas).disp(plain=True, vrange=[0, 255])
plot_box(lbrt=[1.5, 1.5, 4.5, 4.5], color='red')

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------ #

im = np.full((5,5), 0, dtype='uint8')
im[:, 2:] = 255

canvas = np.full((7, 55), 128, dtype='uint8')
canvas[1:6, 1:6] = im
count = 2
for v in range(1, 4):
    for u in range(1, 4):
        W = im[v-1:v+2, u-1:u+2]

        k = count * 5
        canvas[2:5, k:k+3] = W
        count += 1

Image(canvas).disp(plain=True, vrange=[0, 255])
plot_box(lbrt=[1.5, 1.5, 4.5, 4.5], color='red')
rvcprint.rvcprint(subfig='b')

# ------------------------------------------------------------------------ #

im = np.full((5,5), 0, dtype='uint8')
im[2,2] = 255

canvas = np.full((7, 55), 128, dtype='uint8')
canvas[1:6, 1:6] = im
count = 2
for v in range(1, 4):
    for u in range(1, 4):
        W = im[v-1:v+2, u-1:u+2]

        k = count * 5
        canvas[2:5, k:k+3] = W
        count += 1

Image(canvas).disp(plain=True, vrange=[0, 255])
plot_box(lbrt=[1.5, 1.5, 4.5, 4.5], color='red')
rvcprint.rvcprint(subfig='c')

# ------------------------------------------------------------------------ #

im = np.full((5,5), 0, dtype='uint8')
im[2:,2:] = 255

canvas = np.full((7, 55), 128, dtype='uint8')
canvas[1:6, 1:6] = im
count = 2
for v in range(1, 4):
    for u in range(1, 4):
        W = im[v-1:v+2, u-1:u+2]

        k = count * 5
        canvas[2:5, k:k+3] = W
        count += 1

Image(canvas).disp(plain=True, vrange=[0, 255])
plot_box(lbrt=[1.5, 1.5, 4.5, 4.5], color='red')
rvcprint.rvcprint(subfig='d')