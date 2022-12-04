#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3
from spatialmath.base import plot_text

im = Image.Read('eg-morph1.png')
print(im)

S1 = np.ones((5, 5))
e1 = im.morph(S1, 'min')
d1 = e1.morph(S1, 'max')

S2 = np.ones((7, 7))
e2 = im.morph(S2, 'min')
d2 = e2.morph(S2, 'max')

S3 = np.ones((1,13))
e3 = im.morph(S3, 'min')
d3 = e3.morph(S3, 'max')

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
out.disp(black=0.1, axes=False)

plot_text((5, -5), 'input')
plot_text((57, -5), 'after erosion')
plot_text((107, -5), '...then dilation')
plot_text((157, -5), 'SE')

rvcprint.rvcprint()



# results = Image.Tile([im, im, im], columns=1, sep=1, bgcolor=1)
# results.disp(axes=False)
# rvcprint.rvcprint(subfig='a')

# results = Image.Tile([e1, e2, e3], columns=1, sep=1, bgcolor=1)
# results.disp(axes=False)
# rvcprint.rvcprint(subfig='b')

# results = Image.Tile([d1, d2, d3], columns=1, sep=1, bgcolor=1)
# results.disp(axes=False)
# rvcprint.rvcprint(subfig='c')

# SE = Image(np.zeros((results.shape[0], 25), dtype='uint8'))
# SE = SE.paste(S1, [5,15])
# SE = SE.paste(S2, [5,55])
# SE = SE.paste(S3, [5,115])
# results = SE.colorize([255, 0, 0])
# results.disp(axes=False)
# rvcprint.rvcprint(subfig='d')