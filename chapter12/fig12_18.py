#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm

# recompute magnitude from last figure
castle = Image.Read('castle.png', grey=True, dtype='float')
Du = Kernel.DGauss(2)
Iu = castle.convolve(Du)
Iv = castle.convolve(Du.T)
m = (Iu ** 2 + Iv ** 2).sqrt()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.arange(318, 409)
y = np.arange(550, 623)
Y, X = np.meshgrid(y, x)
Z = m.image[318:409, 550:623]
ax.plot_surface(X, Y, Z, cmap=cm.bone,
                       linewidth=0, antialiased=False)
ax.set_xlabel('u')
ax.set_ylabel('v')


# surfl(318:408, 550:622, m(318:408,550:622)')
# colormap(bone)

# xaxis[317,407]
# yaxis[549,621]
ax.set_zlabel('edge magnitude')
ax.view_init(61, 23)

rvcprint.rvcprint()

