#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

b1 = Image.Read('building2-1.png', grey=True)

sf1 = b1.SIFT()

# get the histogram of scales
h, x = np.histogram(sf1.scale, bins=50)

plt.bar(x[1:], h, width=x[1]-x[0])
plt.grid(True)
plt.xlabel('Scale') 
plt.ylabel('Number of occurrences')
plt.yscale('log')  # plot it with log axis
plt.xlim(0, x[-1])
plt.ylim(1, h.max())

rvcprint.rvcprint()

# plt.show(block=True)
