#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9
um = 1e-6

# Figure 10.4 a


plt.figure()
lam = np.linspace(100, 10_000, 100) * nm
e = loadspectrum(lam, 'redbrick')

# TODO add vertical lines

plt.plot(lam / um, e)
plt.xlabel('Wavelength (μm)')
plt.ylabel('R(λ)')


# plot 2 dashed vertical lines
plt.plot([0.4,]*2, [0, 0.6], 'g--')
plt.plot([0.7,]*2, [0, 0.6], 'g--')

plt.xlim(0, 10)
plt.ylim(0, 0.6)

plt.grid()

rvcprint.rvcprint(subfig='a')


# Figure 10.4 b


plt.figure()

lam = np.linspace(400,700,400) * nm
e = loadspectrum(lam, 'redbrick')

# TODO set same y-axis as 10.4a

plt.plot(lam / nm, e)
plt.xlabel('Wavelength (nm)')
plt.ylabel('R(λ)')
plt.xlim(400, 700)
plt.ylim(0, 0.6)
plt.grid()

rvcprint.rvcprint(subfig='b')

# clf
# [R, lambda] = loadspectrum([100:10:10000]*1e-9, 'redbrick.dat')
# plot(lambda*1e6, R)
# xlabel('Wavelength (\mu m)')
# ylabel('R(\lambda)')
# hold on
# vertline(0.4)
# vertline(0.7)
# rvcprint('subfig', 'a', 'thicken', 1.5)

# ##
# [R2, lambda2] = loadspectrum([300:10:700]*1e-9, 'redbrick.dat')
# plot(lambda2*1e9, R2) xaxis(400, 700)
# xlabel('Wavelength (nm)')
# ylabel('R(\lambda)')
# rvcprint('subfig', 'b', 'thicken', 1.5)

