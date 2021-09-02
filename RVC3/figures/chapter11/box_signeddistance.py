#!/usr/bin/env python3

import rvcprint
import numpy as np
# import matplotlib.pyplot as plt
# from machinevisiontoolbox import *
# from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm

from mayavi import mlab

s = np.linspace(-3, 3, 31)

X, Y = np.meshgrid(s, s)

# th, r = cart2pol(X, Y)
r = np.sqrt(X**2 + Y**2)
t = np.arctan2(Y, X)

d = 1- r

f = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(800, 800))

m = mlab.mesh(X, Y, d, figure=f)
mlab.mesh(X, Y, d * 0, color=(1, 0, 0), opacity=0.5, figure=f)
mlab.outline(m)
mlab.axes(m, color=(0, 0, 0), extent=(-3, 3, -3, 3, -3, 1), xlabel='x', ylabel='y', zlabel='f(X)')
f.scene.camera.zoom(0.8)


# mlab.show()

mlab.savefig('box_signeddistance.pdf')
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(X, Y, d * 0, cmap=cm.viridis,
#     rstride=2, cstride=2, edgecolor='none', linewidth=0)

# ax.set_zlim(-3, 1)
# ax.plot_surface(X, Y, d, facecolor='r',
#     rstride=2, cstride=2, edgecolor='none', linewidth=0)

# # surf(X,Y, d*0, 'FaceColor', [1 0 0], 'FaceAlpha', 0.5, 'EdgeColor', 'none')
# plt.xlabel('x')
# plt.ylabel('y')
# ax.set_zlabel('signed distance function')

# # rvcprint.rvcprint(debug=True)
# plt.show(block=True)

