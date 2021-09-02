#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath.base import plot_sphere, plotvol3
from math import pi

u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

fisheye = Image.Read('fisheye_target.png', dtype='float', grey=True)

n = 500
theta_range = np.linspace(0, pi, n)
phi_range = np.linspace(-pi, pi, n)

Phi, Theta = np.meshgrid(phi_range, theta_range)

r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
Us = r * np.cos(Phi) + u0
Vs = r * np.sin(Phi) + v0

spherical = fisheye.interp2d(Us, Vs)

# create 3d Axes
ax = plotvol3()

# ax.plot_surface(x, y, z, facecolors=img.image, cstride=1, rstride=1)

plot_sphere(radius=1, ax=ax, filled=True, resolution=n, 
    facecolors=spherical.colorize().A, cstride=1, rstride=1)

ax.view_init(azim=-143.0, elev=-9)

rvcprint.rvcprint(format='png', interval=0.5)