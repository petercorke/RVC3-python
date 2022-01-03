#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath.base import plot_point

import cv2 as cv


# load linear color image
im_targets = Image.Read('yellowtargets.png', dtype='float', gamma='sRGB')
im_targets.disp()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

# ensure consistent k-means clustering
#  seed OpenCV's random number generator (RNG)

k = 2

ab = im_targets.colorspace('L*a*b*').plane('a*:b*')

ab.plane(1).disp(colorbar=dict(shrink=0.8, aspect=20*0.8))
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

labels, centres, resid = ab.kmeans_color(k, seed=0)
print(resid / ab.npixels)
print(centres)
labels.disp(ncolors=k, colormap='jet', colorbar=dict(shrink=0.8, aspect=20*0.8))
rvcprint.rvcprint(subfig='c')

print([color2name(c, "a*b*") for c in centres.T])

# ----------------------------------------------------------------------- #

plt.clf()
plot_chromaticity_diagram(colorspace='ab')
plot_point(centres, marker='*', text='{}')
rvcprint.rvcprint(subfig='d')

# ----------------------------------------------------------------------- #

objects = (labels == 0)
objects.disp() #black=0.1)
rvcprint.rvcprint(subfig='e')

# ----------------------------------------------------------------------- #

# targets_binary = objects.open(Kernel.Circle(2))
# targets_binary.disp() #black=0.1)
# rvcprint.rvcprint(subfig='f')

plt.close('all')

print([color2name(c, "a*b*") for c in centres.T])
