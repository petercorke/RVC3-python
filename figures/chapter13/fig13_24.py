#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from math import pi

u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

fisheye = Image.Read('fisheye_target.png', dtype='float', mono=True)
fisheye.disp(title=False)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

n = 500
theta_range = np.linspace(0, pi, n)
phi_range = np.linspace(-pi, pi, n)

Phi, Theta = np.meshgrid(phi_range, theta_range)

r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
U = r * np.cos(Phi) + u0
V = r * np.sin(Phi) + v0

import time
t0 = time.time()
spherical = fisheye.warp(U, V, domain=(phi_range, theta_range))
# much slower, but can flag extrapolated values
# spherical = fisheye.interp2d(Us, Vs)
print(time.time() - t0)

spherical.disp()
plt.gca().set_aspect('auto')
plt.xlabel(r'$\bf \phi$ (rad)')
plt.ylabel(r'$\bf \theta$ (rad)')
rvcprint.rvcprint(subfig='b')

