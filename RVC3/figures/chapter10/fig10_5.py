#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

plt.figure()
lam = np.linspace(400, 700, 400) * nm
e = loadspectrum(lam, 'solar')
r = loadspectrum(lam, 'redbrick')

l = e * r

plt.plot(lam / nm, l)
plt.xlabel('Wavelength (nm)')
plt.ylabel(r'L(λ) $(W sr^{-1} m^{-2} m^{-1}) \times 10^{8}$')
plt.xlim(400, 700)
plt.grid()
plt.show()


# lambda = [400:10:700]*1e-9        # visible spectrum
# E = loadspectrum(lambda, 'solar.dat')
# R = loadspectrum(lambda, 'redbrick.dat')
# L = E .* R
# plot(lambda*1e9, L)
# xlabel('Wavelength (nm)')
# ylabel('W sr^{-1} m^{-2} m^{-1}')
# xaxis(400, 700)

rvcprint.rvcprint()
