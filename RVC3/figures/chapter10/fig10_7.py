#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

lam = np.arange(350, 750) * nm
human = luminos(lam)

plt.figure()

plt.plot(lam / nm, human, color='tab:blue',label='human')
plt.ylabel('Photopic luminosity (lm/W)')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.ylim(0, 700)
plt.grid()
rvcprint.rvcprint(subfig='b')

cones = loadspectrum(lam, 'cones')
plt.figure()
plt.plot(lam / nm, cones[:, 0], 'r')
plt.plot(lam / nm, cones[:, 1], 'g')
plt.plot(lam / nm, cones[:, 2], 'b')
plt.ylabel('$\mathbf{L(\lambda)}$ normalized cone response')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.ylim(0, 1)
plt.grid()
plt.legend(['red (L) cone', 'green (M) cone', 'blue (S) cone'])

rvcprint.rvcprint(subfig='a')


