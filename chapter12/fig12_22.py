#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm
import spatialmath.base as smb


crowd = Image.Read('wheres-wally.png', grey=True, dtype='float')
crowd.disp()

T = Image.Read('wally.png', grey=True, dtype='float')
T.disp()

sim = crowd.similarity(T, 'zncc')
sim.disp() #colorbar=True)
# c = colorbar
# c.Label.String = 'similarity'
# c.Label.FontSize = 10

maxima = sim.peak2(scale=2, npeaks=5)
maxima.xy
smb.plot_circle(maxima.xy, radius=30, color='y', filled=True, alpha=0.4)
smb.plot_point(maxima.xy, color='k', marker='none', text="{}", textargs={'fontweight': 'bold', 'fontsize': 16})
plt.xlim(0, sim.width)
plt.ylim(sim.height, 0)

rvcprint.rvcprint()
