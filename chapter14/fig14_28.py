#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, DSI = L.DSI(R, 3, [40, 90])

mx = np.nanmax(DSI[:, 90:, :], axis=2)

h, x = np.histogram(mx, 100)
cdf = h.cumsum()
cdf = cdf / cdf[-1]

dx = x[1] - x[0]
plt.bar(x[1:] - dx / 2, cdf, width=dx)
# histogram(sim(:), 'Normalization', 'cdf', 'EdgeColor', 'none')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid(True)
plt.xlabel('ZNCC similarity')
plt.ylabel('Cumulative distribution')
plt.gca().axvline(0.6, color='r', linestyle='--')
plt.gca().axvline(0.9, color='r', linestyle='--')

rvcprint.rvcprint(debug=True)
