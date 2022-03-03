#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, similarity, DSI = L.stereo_simple(R, 3, [40, 90])

mx = np.nanmax(DSI[:, 90:, :], axis=2)

plt.hist(similarity.view1d(), 100, (0, 1), cumulative=True, density=True)
# histogram(sim(:), 'Normalization', 'cdf', 'EdgeColor', 'none')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid(True)
plt.xlabel('ZNCC similarity')
plt.ylabel('Cumulative distribution')
plt.gca().axvline(0.6, color='r', linestyle='--')
plt.gca().axvline(0.9, color='r', linestyle='--')

rvcprint.rvcprint()
