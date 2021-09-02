#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


im1 = Image.Read('eiffel2-1.png', grey=True)

pks, _ = im1.harriscorner(nfeat=200)
im1.disp(grid=True, darken=True, title=False)
pks, _ = im1.harriscorner(nfeat=250, hw=2, scale=7)
plot_point(pks[:, :2].T, marker='sy', markerfacecolor='none')
rvcprint.rvcprint(subfig='a')

plt.clf()
im1.disp(grid=True, darken=True, title=False)

sf = im1.SIFT().filter(percentstrength=20, minscale=10)
sf.plot(alpha=0.3)
rvcprint.rvcprint(subfig='b')
