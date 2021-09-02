#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

castle = Image.Read('castle2.png', dtype='float')

castle.disp()
rvcprint.rvcprint(subfig='a')

t = castle.otsu()
print(t)

h = castle.hist()
h.plot()
plt.grid(True)
plt.gca().axvline(t, color='r', linestyle='--')
plt.gca().axvline(0.75, color='r', linestyle='--')
rvcprint.rvcprint(subfig='b')

castle.thresh(0.75).disp(black=0.3)
rvcprint.rvcprint(subfig='c')

castle.thresh(t).disp(black=0.3)
rvcprint.rvcprint(subfig='d')

