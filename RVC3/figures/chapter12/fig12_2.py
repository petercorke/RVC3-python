#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

castle = Image.Read('castle.png', dtype='float')

castle.disp()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

castle.thresh(0.7).disp(black=0.1)
rvcprint.rvcprint(subfig='b')
# ----------------------------------------------------------------------- #

t = castle.otsu()
print(t)

plt.clf()
castle.hist().plot()
plt.grid(True)
plt.gca().axvline(0.7, color='b', linestyle='--', label='0.7')
plt.gca().axvline(t, color='r', linestyle='--', label='Otsu threshold')
plt.legend()
rvcprint.rvcprint(subfig='c')


# ----------------------------------------------------------------------- #

castle.thresh(t).disp(black=0.1)
rvcprint.rvcprint(subfig='d')
