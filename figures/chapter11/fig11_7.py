#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3

church = Image.Read('church.png', grey=True)

h = church.hist()
h.plot()
plt.grid(True)
ylim = plt.gca().get_ylim()
plt.plot([180, 180], ylim, 'b--')
rvcprint.rvcprint(subfig='a')

plt.clf()
h.plot('ncdf', color='b')
hn = church.normhist().hist()
hn.plot('ncdf', color='r')
plt.legend(['original', 'normalized'])
plt.grid(True)
plt.xlim(0, 255)
plt.ylabel('cumulative number of pixels')

rvcprint.rvcprint(subfig='b')

