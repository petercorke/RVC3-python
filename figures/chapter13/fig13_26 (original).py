#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from math import pi
from spatialmath import SE3
import math

u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

fisheye = Image.Read('fisheye_target.png', dtype='float', mono=True)
fisheye.disp()


n = 500
theta_range = np.linspace(0, pi, n)
phi_range = np.linspace(-pi, pi, n)

Phi, Theta = np.meshgrid(phi_range, theta_range)

r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
U = r * np.cos(Phi) + u0
V = r * np.sin(Phi) + v0

spherical = fisheye.warp(U, V)


## 11.4.2  Mapping from the sphere to a perspective image

W = 1000
m = W / 2 / math.tan(np.radians(45 / 2))

l = 0

u0 = W / 2; v0 = W/2;

# span the output image
Uo, Vo = np.meshgrid(np.arange(W), np.arange(W))

U0 = Uo - u0
V0 = Vo - v0
phi = np.arctan2(V0, U0)
r = np.sqrt(U0 ** 2 + V0 ** 2)

# convert to Phi, Theta coordinates
Phi_o = phi
Theta_o = pi - np.arctan(r / m)

perspective = spherical.interp2d(Phi_o, Theta_o, Phi, Theta)
perspective.disp(badcolor='red')

rvcprint.rvcprint(subfig='a')


nPhi, nTheta = base.sphere_rotate(Phi, Theta, SE3.Ry(0.9)*SE3.Rz(-1.5))

# warp the image
spherical2 = spherical.interp2d(nPhi, nTheta, Phi, Theta)

perspective = spherical2.interp2d(Phi_o, Theta_o, Phi, Theta)
perspective.disp(badcolor='red')

rvcprint.rvcprint(subfig='b')


