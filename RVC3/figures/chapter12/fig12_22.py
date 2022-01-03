#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('church.png', grey=True)
edges = im.canny()
h = edges.Hough()

im.disp(grid=True, darken=True, title=False)
lines = h.lines_p(100, 200, 5, seed=0)
print(lines.shape)
h.plot_lines_p(lines, 'r--')


# plt.show(block=True)

rvcprint.rvcprint()

