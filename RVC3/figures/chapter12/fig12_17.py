#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('5points.png')
print(im)
im.disp(black=0.3, title=False, grid=True)
rvcprint.rvcprint(subfig='a')

h = Hough(im, 90, 2)

h.plot_accumulator()
cbar = plt.colorbar()
cbar.set_label('Votes')
rvcprint.rvcprint(subfig='b')