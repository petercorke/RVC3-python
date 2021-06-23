#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

b1 = Image.Read('building2-1.png', grey=True, dtype='float')
b1.disp(darken=True)
pks, C = b1.harriscorner(nfeat=200, hw=2, scale=7)
C.disp(colormap='signed', grid=True)
plot_point(pks[:, :2].T, marker='sk', markerfacecolor='none')
plt.xlim(600, 800)
plt.ylim(400, 200)

rvcprint.rvcprint(subfig='a')


# rvcprint.rvcprint(subfig='b')

# idisp(strength,  'invsigned', 'nogui')
# C.plot('ks')
# axis([300 500 300 500])
# rvcprint.rvcprint(subfig='a', 'svg')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xc = 420
yc = 390
n = 35
x = np.arange(xc-n, xc+n)
y = np.arange(yc-n, yc+n)
X, Y = np.meshgrid(x, y)
Z = C.asfloat()[yc-n:yc+n, xc-n:xc+n]
# xnew = np.linspace(xc-n, xc+n, 200)
# ynew = np.linspace(yc-n, yc+n, 200)
# Xnew, Ynew = np.meshgrid(xnew, ynew)

# from scipy import interpolate
# tck = interpolate.bisplrep(X, Y, Z, s=0.01)
# Znew = interpolate.bisplev(xnew, ynew, tck)

# ax.plot_surface(Xnew, Ynew, Znew, cmap=cm.RdBu, cstride=1, rstride=1, alpha=1)

ax.plot_surface(X, Y, Z, cmap=cm.RdBu, cstride=1, rstride=1, alpha=1)
plt.xlabel('u (pixels)')
plt.ylabel('v (pixels)')
ax.set_zlabel('corner strength')
ax.view_init(32, 160)
rvcprint.rvcprint(subfig='b')

# plt.show(block=True)

