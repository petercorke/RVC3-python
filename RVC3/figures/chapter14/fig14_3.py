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
print(m[:5])

m[:100].plot('y', width=200, linewidth=0.7)
# Image.ColorOverlay(sf1._image, sf2._image)

rvcprint.rvcprint(thicken=None)

# plt.show(block=True)