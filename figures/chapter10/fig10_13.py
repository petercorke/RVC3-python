#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9


lam = np.arange(350, 750) * nm
cmf = cmfxyz(lam)

plt.plot(lam / nm, cmf)

plt.ylabel('color matching functions')
plt.xlabel('Wavelength (nm)')
plt.grid()
plt.xlim(350, 750)
plt.ylim(0, 1.8)
plt.legend(labels=(r'$\bar{x}$', r'$\bar{y}$', r'$\bar{z}$'))

plt.show()

rvcprint.rvcprint(subfig='a')

plt.clf()



plot_chromaticity_diagram('xy')
plt.grid(True)
# lam = np.arange(350, 750) * nm
# xy = lambda2xy(lam)
# print(xy)
# print(xy.shape)
# plt.plot(xy[0:, 0], xy[0:, 1], linewidth=1)  
# following fig10_13.m, colorspace looks a bit different...


# plt.show(block=True)
rvcprint.rvcprint(subfig='b')

