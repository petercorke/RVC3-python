#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3, base
import cv2 as cv

images = ImageCollection('calibration/*.jpg')

K, distortion, frames = CentralCamera.images2C(images, gridshape=(7,6), squaresize=0.025)

cam = CentralCamera()

ax = base.plotvol3([-0.1, 0.3, -0.1, 0.3, -0.4, 0])
for frame in frames:
    cam.plot(pose=frame.pose, scale=0.05, shape='camera')
    ax.text(*frame.pose.t, f" {frame.id}", zorder=20, fontsize=12)
shape = np.r_[7 * 0.025, 6 * 0.025, 0.01]
base.plot_cuboid(shape, centre=shape/2)

rvcprint.rvcprint(subfig='a', interval=(0.1, 0.1, 0.05))
#----------------------------------------------------------------------- #

distorted = images[11]

k = distortion[[0, 1, 4]]; p = distortion[[2, 3]]
u0, v0 = K[:2, 2]
fpix_u = K[0, 0]
fpix_v = K[1, 1]

Ud, Vd = distorted.meshgrid()
u = (Ud - u0) / fpix_u;
v = (Vd - v0) / fpix_v;

r = np.sqrt( u**2 + v**2 );
delta_u = u * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*u*v + p[1]*(r**2 + 2*u**2)
delta_v = v * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*(r**2 + 2*v**2) + p[1]*u*v

ud = u + delta_u; vd = v + delta_v;

U = ud * fpix_u + u0;
V = vd * fpix_v + v0;

plt.clf()
cx, cy = [int(c) for c in distorted.centre]
sx = cx % 50
sy = cy % 50
plt.quiver(U[sy::50, sx::50], V[sy::50, sx::50],
    -delta_u[sy::50, sx::50], -delta_v[sy::50, sx::50])

dmag = np.sqrt(delta_u**2 + delta_v**2)
plt.contour(U, V, dmag)

plt.plot(u0, v0, '+', markersize=16)
plt.grid(True)
plt.xlabel('u (pixels')
plt.ylabel('v (pixels')
rvcprint.rvcprint(subfig='c')