#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm
from spatialmath.base import plot_circle, plot_point


crowd = Image.Read('wheres-wally.png', grey=True, dtype='float')
crowd.disp()

T = Image.Read('wally.png', grey=True, dtype='float')
T.disp()

sim = crowd.similarity(T, 'zncc')
sim.disp(colormap='signed', colorbar=dict(label='ZNCC'))
# c = colorbar
# c.Label.String = 'similarity'
# c.Label.FontSize = 10

maxima, location = sim.peak2d(scale=2, npeaks=5)
print(maxima)
# smb.plot_circle(centre=maxima[:, :2].T, radius=30, color='y', filled=True, alpha=0.4)
# smb.plot_point(maxima[:, :2].T, color='none', marker='none', text="{}", textargs={'fontweight': 'bold', 'fontsize': 16})


plot_circle(centre=location, radius=20, color="k");
plot_point(location, color="none", marker="none", text="  #{}");


plt.xlim(0, sim.width)
plt.ylim(sim.height, 0)

rvcprint.rvcprint()
