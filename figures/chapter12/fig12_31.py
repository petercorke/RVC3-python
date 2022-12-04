#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

b1 = Image.Read('building2-1.png', grey=True)
b1.disp(darken=True, grid=True)

sf1 = b1.SIFT().filter(percentstrength=50, minscale=5)
print(sf1[:20])
sf1.plot(filled=True, color='y', hand=True, alpha=0.3)

rvcprint.rvcprint()
# plt.show(block=True)