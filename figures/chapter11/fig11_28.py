#!/usr/bin/env python3

# now dilate


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath.base import plot_text

im = Image.Read('eg-morph2.png')

S1 = np.ones((5, 5))
e1 = im.morph(S1, 'max')
d1 = e1.morph(S1, 'min')

S2 = np.ones((7, 7))
e2 = im.morph(S2, 'max')
d2 = e2.morph(S2, 'min')

S3 = np.ones((1,13))
e3 = im.morph(S3, 'max')
d3 = e3.morph(S3, 'min')

# create tile for first 3 columns
results = Image.Tile([im, e1, d1, im, e2, d2, im, e3, d3], columns=3, sep=1, bgcolor=1)

# stack the structuring elements
SE = Image.Zeros(25, results.shape[0], dtype='uint8')
SE = SE.paste(S1, [5,15])
SE = SE.paste(S2, [5,55])
SE = SE.paste(S3, [5,115])

# colorize and stack horizontally
results = results.colorize([255, 255, 255])
SE = SE.colorize([255, 0, 0])
out = Image.Hstack([results, SE], sep=1, bgcolor=[255, 255, 255])

# display it, and add text labels
out.disp(black=0.1, axes=False, interpolation='nearest')

plot_text((5, -5), 'input')
plot_text((57, -5), 'after dilation')
plot_text((107, -5), '...then erosion')
plot_text((157, -5), 'SE')

rvcprint.rvcprint()
