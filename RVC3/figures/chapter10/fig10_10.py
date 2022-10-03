#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

lam = np.arange(350, 800, 5) * nm
cmf = cmfrgb(lam, method='cubic')

plt.plot(lam / nm, cmf[:,0], 'r', label=r'$\bar{r}(\lambda)$')
plt.plot(lam / nm, cmf[:,1], 'g', label=r'$\bar{g}(\lambda)$')
plt.plot(lam / nm, cmf[:,2], 'b', label=r'$\bar{b}(\lambda)$')
plt.ylabel('color matching functions')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.grid()
plt.legend()

rvcprint.rvcprint(subfig='a')

plt.clf()
ax = plt.gcf().add_subplot(1, 1, 1, projection='3d')
ax.view_init(30, -44)

plt.plot(cmf[:,0], cmf[:,1], 0 * cmf[:,2], 'r')
plt.plot(cmf[:,0], cmf[:,1], cmf[:,2], 'k--')
ax.set_xlabel(r'$\mathbf{\bar{r}(\lambda)}$')
ax.set_ylabel(r'$\mathbf{\bar{g}(\lambda)}$')
ax.set_zlabel(r'$\mathbf{\bar{b}(\lambda)}$')
for lam in np.arange(400, 700, 50):
    c = cmfrgb(lam * nm)
    ax.plot(c[0], c[1], c[2], 'ko')
    ax.text(c[0], c[1], c[2], f" {lam}")


rvcprint.rvcprint(subfig='b')

