#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


b1 = Image.Read('building2-1.png', grey=True, dtype='float')
harris = b1.Harris(nfeat=500)


h, x = np.histogram(harris.strength, 100)
cdf = np.cumsum(h)
cdf = cdf / cdf[-1]
plt.bar(x[1:], cdf, width=x[1]-x[0])
print(x)

# histogram(s(:), 'Normalization', 'cdf', 'EdgeColor', 'none')
# #xaxis(max(x)) yaxis(0.8, 1)
# yaxis(0.5, 1)
plt.gca().axvline(x[-1] / 2, color='r', linestyle='--')
plt.xlabel('Corner strength')
plt.xlim(0, x[-1])
plt.ylim(0, 1)
plt.ylabel('Cumulative number of features')
plt.grid(True)
#(1-interp1(x, ch, strongest/2))*100

rvcprint.rvcprint()


