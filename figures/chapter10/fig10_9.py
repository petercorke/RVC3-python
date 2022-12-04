#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.patches import Polygon
from matplotlib.ticker import ScalarFormatter

nm = 1e-9

lam = np.arange(350, 800, 5) * nm
E = loadspectrum(lam, 'solar')
R = loadspectrum(lam, 'redbrick')
C = loadspectrum(lam, 'cones')

ax0 = plt.subplot(3,1,1)
ax0.plot(lam / nm, E, linewidth=2)
plt.xlim(350, 750)
ax0.xaxis.set_ticklabels([])

ax0.grid()
ax0.set_ylabel('illuminance')
ax0.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))

L = np.squeeze(E * R)

ax1 = plt.subplot(3,1,2)
ax1.plot(lam / nm, L * 1, linewidth=2)
plt.xlim(350, 750)
ax1.grid()
ax1.set_ylabel('luminance')
ax1.xaxis.set_ticklabels([])
ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))


alpha = 0.7

#B = np.squeeze(L) * C.s[:,0]
#for i in range(len(C.s[:,0])):
#    print('{0:.8f}'.format(B[i]))

ax2 = plt.subplot(3,1,3)
# TODO should be plotted using area()
# TODO make this into a giant polygon - joint first/last pt, join them across to form the polygon
# use alpha = 0.5
p0 = np.transpose(np.vstack((lam / nm, nm * L * C[:, 0])))
#print(p0)
#print(p0.shape)
poly0 = Polygon(p0, closed=True, facecolor='r', linestyle='-', alpha=0.75)
ax2.add_patch(poly0)

p1 = np.transpose(np.vstack((lam / nm, nm * L * C[:, 1])))
poly1 = Polygon(p1, closed=True, facecolor='g', linestyle='-', alpha=0.75)
ax2.add_patch(poly1)

p2 = np.transpose(np.vstack((lam / nm, nm * L * C[:, 2])))
poly2 = Polygon(p2, closed=True, facecolor='b', linestyle='-', alpha=0.75)
ax2.add_patch(poly2)

ax2.plot(lam / nm, nm * L * C[:,0], color='r', linewidth=1.5, alpha=0)  # addpatch (above) seems to require a plot, so workaround is to plot something and make alpha = 0
ax2.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))

# ax2.plot(lam / nm, L * C.s[:,1], color='g', linewidth=1.5)
# ax2.plot(lam / nm, L * C.s[:,2], color='b', linewidth=1.5)
ax2.set_ylabel('cone response')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
ax2.grid()

rvcprint.rvcprint(subfig='b', format='pdf')
