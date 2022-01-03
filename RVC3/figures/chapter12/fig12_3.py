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

# ----------------------------------------------------------------------- #

t = castle.otsu()
print(t)

castle.thresh(t).disp(black=0.1)
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #



plt.clf()
h = castle.hist()
h.plot()
plt.grid(True)
plt.gca().axvline(0.79, color='b', linestyle='--', label='0.79')
plt.gca().axvline(t, color='r', linestyle='--', label='Otsu threshold')
plt.legend()
rvcprint.rvcprint(subfig='c')


# ----------------------------------------------------------------------- #

castle.thresh(0.79).disp(black=0.1)
rvcprint.rvcprint(subfig='d')

