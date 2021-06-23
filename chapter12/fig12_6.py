#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


# load linear color image
im_targets = Image.Read('yellowtargets.png', dtype='float', gamma='sRGB')
im_targets.disp()
rvcprint.rvcprint(subfig='a')

# ensure consistent k-means clustering
#  seed OpenCV's random number generator (RNG)
cv.setRNGSeed(0)

k = 2

ab = im_targets.colorspace('Lab').plane('ab')

labels, centres, _ = ab.colorkmeans(k)
labels.disp(ncolors=k, colormap='jet', colorbar=True)
rvcprint.rvcprint(subfig='b')

plt.clf()
plot_chromaticity_diagram(colorspace='ab')
plot_point(centres.T, marker='*', text='{}')
rvcprint.rvcprint(subfig='c')

objects = (labels == 0)
objects.disp(black=0.3)
rvcprint.rvcprint(subfig='d')

targets_binary = objects.open(Kernel.Circle(2))
targets_binary.disp(black=0.3)
rvcprint.rvcprint(subfig='e')

plt.close('all')
