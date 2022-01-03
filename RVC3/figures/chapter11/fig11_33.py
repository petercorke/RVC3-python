#!/usr/bin/env python3
    
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm

im = Image.Squares(1, size=256).rotate(0.3).canny()
im.disp()
rvcprint.rvcprint(subfig='a')


dx = im.distance_transform()
dx.disp(colorbar=dict(label='Euclidean distance (pixels)'))

corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1],  [-1, -1]])
corners = corners*64 + 128
plt.plot(corners[:,0], corners[:,1], color='r', linewidth=2)

rvcprint.rvcprint(subfig='b', thicken=None)

fig = plt.figure()
X, Y = np.meshgrid(np.arange(256), np.arange(256))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, dx.image, cmap=cm.viridis,
    rstride=2, cstride=2, edgecolor='none', linewidth=0)

corners = np.hstack((corners, 20 * np.ones((5,1))))
ax.plot(corners[:,0], corners[:,1], corners[:,2], color='r', linewidth=2)
ax.set_xlabel('u (pixels)')
ax.set_ylabel('v (pixels)')
ax.set_zlabel('Euclidean distance (pixels)')
ax.view_init(40, -105)

rvcprint.rvcprint(subfig='c')
