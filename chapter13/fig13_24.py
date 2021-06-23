#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from math import pi

u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

fisheye = Image.Read('fisheye_target.png', dtype='float', grey=True)
fisheye.disp(title=False)

rvcprint.rvcprint(subfig='a')

n = 500
theta_range = np.linspace(0, pi, n)
phi_range = np.linspace(-pi, pi, n)

Phi, Theta = np.meshgrid(phi_range, theta_range)

r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
Us = r * np.cos(Phi) + u0
Vs = r * np.sin(Phi) + v0

spherical = fisheye.interp2d(Us, Vs)

spherical.disp(badcolor='red')

rvcprint.rvcprint(subfig='b')