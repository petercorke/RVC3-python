#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3

ax = plt.subplot(2, 2, 1)
# im = testpattern('rampx', 256, 2)
im = Image.Ramp(cycles=2, size=500, dir='x')

im.disp(ax=ax, plain=True)

ax = plt.subplot(2, 2, 2)
# im = testpattern('siny', 256, 2)
im = Image.Sin(cycles=5, size=500, dir='y')
im.disp(ax=ax, plain=True)

ax = plt.subplot(2, 2, 3)
im = Image.Squares(5, 500)
im.disp(ax=ax, plain=True)

ax = plt.subplot(2, 2, 4)
# im = testpattern('dots', 256, 256, 100)
im = Image.Circles(2, 500)

im.disp(ax=ax, plain=True)

# rvcprint.rvcprint(subfig='a')


canvas = Image.Zeros(1000, 1000)
sq1 = Image.Constant(150, 150, 0.5)
sq2 = Image.Constant(80, 80, 0.9)
canvas.paste(sq1, [100, 100])
canvas.paste(sq2, [300, 300])
circle = 0.6 * Kernel.Circle(120)
canvas.paste(circle, [600, 200])
# canvas = iline( canvas, [100 100], [800 800], 0.8)
canvas.disp(black=0.2)

rvcprint.rvcprint(subfig='b')

