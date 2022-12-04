#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

b1 = Image.Read('building2-1.png', grey=True, dtype='float')

harris = b1.Harris(nfeat=500)
b1.disp(darken=True, title=False)
harris.plot()
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

plt.xlim(400, 900)
plt.ylim(350, 50)
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

b2 = Image.Read('building2-2.png', grey=True, dtype='float')

harris = b2.Harris(nfeat=500)
b2.disp(darken=True, title=False)
harris.plot()
rvcprint.rvcprint(subfig='c')

# ----------------------------------------------------------------------- #

plt.xlim(200, 700)
plt.ylim(350, 50)
rvcprint.rvcprint(subfig='d')

# plt.show(block=True)


