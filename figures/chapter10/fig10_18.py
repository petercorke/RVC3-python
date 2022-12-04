#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter

nm = 1e-9

lam = np.arange(400, 701, 5) * nm

R = loadspectrum(lam, 'redbrick')
sun = loadspectrum(lam, 'solar')
A = loadspectrum(lam, 'water')

d = 2
T = 10 ** (-d*A)
L = sun * R * T

plt.plot(lam / nm, L, 'b')
plt.plot(lam / nm, sun * R, 'r')
plt.xlim(400, 700)
plt.legend(['underwater', 'in air'])
plt.xlabel('Wavelength (nm)')
plt.ylabel('Luminance L(λ)')
plt.grid()
plt.xlim(400, 700)
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))


# plt.show(block=True)
rvcprint.rvcprint()
