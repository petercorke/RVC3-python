#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv
from spatialmath.base import plot_point

# load linear color image
im_targets = Image.Read('tomato_124.png', dtype='float', gamma='sRGB')
im_targets.disp()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

# ensure consistent k-means clustering
#  seed OpenCV's random number generator (RNG)
cv.setRNGSeed(0)

k = 3

ab = im_targets.colorspace('L*a*b*').plane('a*:b*')

ab.plane(0).disp(colorbar=dict(shrink=0.8, aspect=20*0.8))
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

labels, centres, _ = ab.kmeans_color(k)
labels.disp(ncolors=k, colormap='jet', colorbar=dict(shrink=0.8, aspect=20*0.8))
rvcprint.rvcprint(subfig='c')

print([color2name(c, "a*b*") for c in centres.T])
# ----------------------------------------------------------------------- #

plt.clf()
plot_chromaticity_diagram(colorspace='ab')
plot_point(centres, marker='*', text='{}')
rvcprint.rvcprint(subfig='d')

objects = (labels == 2)
objects.disp() #black=0.1)
rvcprint.rvcprint(subfig='e')

# ----------------------------------------------------------------------- #

tomatoes_binary = objects.close(Kernel.Circle(15))
tomatoes_binary.disp() #black=0.1)
rvcprint.rvcprint(subfig='f')

plt.close('all')
