#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import scipy as sp
import spatialmath.base as smb


im = Image.Read('scale-space.png', dtype='float')
im.disp(square=True, black=0.1, grid=True, title=False)

G, L, s = im.scalespace(60, 2)
z = np.stack([np.abs(Lk.image) for Lk in L], axis=2)
features = findpeaks3d(z, npeaks=4)
print(features)

for v, u, i, _ in features:
    plt.plot(u, v, 'k+')
    scale = s[int(i)]
    smb.plot_circle(radius=scale * np.sqrt(2), centre=(u,v), color='y')

rvcprint.rvcprint()
