#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

sf1 = Image.Read('eiffel-1.png').SIFT()
sf2 = Image.Read('eiffel-2.png').SIFT()
m = sf1.match(sf2)

n, x, _ = plt.hist(m.distance, bins=100, cumulative=True, density=True)

# h, x = np.histogram(m.distance, bins=100)
# cdf = np.cumsum(h)
# cdf = cdf / cdf[-1]
# dx = x[1] - x[0]
# plt.bar(x[1:] - dx / 2, cdf, width=dx)
plt.xlabel('SIFT descriptor distance')
plt.ylabel('Cumulative distributon')
plt.grid(True)
plt.ylim(0, 1)
plt.xlim(0, x[-1])

plt.gca().axvline(75, color='r', linestyle='--')

rvcprint.rvcprint()
