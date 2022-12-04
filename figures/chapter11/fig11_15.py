#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm


h = 15

K = Kernel.Gauss(5, h=h)
idisp(K, title=None)
plt.xlabel('u')
plt.ylabel('v')
rvcprint.rvcprint(subfig='a')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.arange(-h, h + 1)
y = np.arange(-h, h + 1)
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, K,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')
rvcprint.rvcprint(subfig='b')

ax.clear()
K = Kernel.Circle(8, 15);
ax.plot_surface(X, Y, K,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')
rvcprint.rvcprint(subfig='c')

K = Kernel.DGauss(5);
ax.clear()
ax.plot_surface(X, Y, K,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')
rvcprint.rvcprint(subfig='d')


K = Kernel.LoG(5);
ax.clear()
ax.plot_surface(X, Y, K,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')
rvcprint.rvcprint(subfig='e')

K = Kernel.DoG(4, 4*1.6, 15);
ax.clear()
ax.plot_surface(X, Y, K,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')
rvcprint.rvcprint(subfig='f')

# plt.show(block=True)
