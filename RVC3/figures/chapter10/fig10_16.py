#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

λ = np.arange(400, 701, 10) * nm
R = loadspectrum(λ, 'redbrick')

sun = loadspectrum(λ, 'solar')
lamp = blackbody(λ, 2_600)

xy_sun = lambda2xy(λ, sun * R)
xy_lamp = lambda2xy(λ, lamp * R)


plot_chromaticity_diagram('xy')

plt.plot(xy_sun[0], xy_sun[1], 'k*', markersize=6)
plt.plot(xy_lamp[0], xy_lamp[1], 'ko', markersize=5)

A = loadspectrum(λ, 'water')
d = 2
T = 10.0 ** (-d * A)
L = sun * R * T
xy_water = lambda2xy(λ, L)
plt.plot(xy_water[0], xy_water[1], 'kd', markersize=5)

plt.legend(['sun', 'tungsten', 'underwater'])
plt.grid()
rvcprint.rvcprint()


