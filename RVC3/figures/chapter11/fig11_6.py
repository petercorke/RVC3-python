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

rvcprint.rvcprint(subfig='a')


canvas = Image.Zeros(1000, 1000, dtype='uint8')

canvas.draw_box(lb=(100, 100), wh=(150, 150), color=100, thickness=-1)
canvas.draw_box(lb=(300, 300), wh=(80, 80), color=150, thickness=-1)
canvas.draw_circle((600, 600), 120, color=200, thickness=-1)
canvas.draw_line((100, 100), (800, 800), color=250, thickness=8)
canvas.disp() #black=0.2)

rvcprint.rvcprint(subfig='b')

