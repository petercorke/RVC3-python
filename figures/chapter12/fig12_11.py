#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath.base import *


sharks = Image.Read('sharks.png')
blobs = sharks.blobs()

labels, n = sharks.labels_binary()
shark = labels == 3

shark.disp() # black=0.1
u, v = shark.nonzero()

umin = u.min()
umax = u.max()
vmin = v.min()
vmax = v.max()

plot_box(lbrt=[umin, vmin, umax, vmax], color='y')

# moments = shark.moments()
# print(moments)

# m00 = moments['m00']
# uc = moments['m10'] / m00
# vc = moments['m01'] / m00
# plot_point((uc, vc), marker=['ok', 'xk'], markerfacecolor='none')

# u20 = moments['mu20']
# u02 = moments['mu02']
# u11 = moments['mu11']

m00 = shark.mpq(0, 0)
uc = shark.mpq(1, 0) / m00
vc = shark.mpq(0, 1) / m00

plot_point((uc, vc), marker=["ob", "xb"], markerfacecolor='none')


u20 = shark.upq(2, 0)
u02 = shark.upq(0, 2)
u11 = shark.upq(1, 1)

J = np.array([[u20, u11], [u11, u02]])
lmbda, x = np.linalg.eig(J)
ab = 2 * np.sqrt(lmbda / m00)
print(ab[0] / ab[1])
print('eigs', lmbda)
print('eigval', x)
v = x[:, 0]
np.arctan2(v[1], v[0])

plot_ellipse(4 * J / m00, centre=(uc, vc), inverted=True, color='c', linewidth=2)

rvcprint.rvcprint(subfig='a')
# ----------------------------------------------------------------------- #


plt.xlim(400, 600)
plt.ylim(300, 100)
rvcprint.rvcprint(subfig='b', thicken=2)

