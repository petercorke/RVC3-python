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
# h, x = np.histogram(sf1.scale, bins=50)

# plt.bar(x[1:], h, width=x[1]-x[0])
x = sf1.scale
plt.hist(x, bins=50)
plt.grid(True)
plt.xlabel('Scale') 
plt.ylabel('Number of occurrences')
plt.yscale('log')  # plot it with log axis
plt.xlim(0, max(x))
# plt.ylim(1, h.max())

rvcprint.rvcprint()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# Z, x, y = np.histogram2d(sf1.scale, sf1.strength, bins=(50, 50))
# X, Y = np.meshgrid(x[1:], y[1:])
# ax.plot_surface(np.log10(X), Y, Z.T, cmap=cm.coolwarm, cstride=1, rstride=1, alpha=1)
# plt.xlabel(r'$\log_{10}(scale)$')
# plt.ylabel('strength')
# plt.grid(True)

# rvcprint.rvcprint(subfig='b')

# from scipy import interpolate
# xnew = np.linspace(x[0], x[-1], 200)
# ynew = np.linspace(y[0], y[-1], 200)
# Xnew, Ynew = np.meshgrid(xnew, ynew)
# tck = interpolate.bisplrep(X, Y, Z, s=0.01)
# Znew = interpolate.bisplev(xnew, ynew, tck)
# ax.plot_surface(Xnew, Ynew, Znew.T, cmap=cm.coolwarm, cstride=5, rstride=5, alpha=1)


# plt.figure()
# plt.plot(sf1.scale, sf1.strength, '.')
# plt.xlabel('scale')
# plt.ylabel('strength')
# plt.grid(True)

