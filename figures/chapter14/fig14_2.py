#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

view1 = Image.Read('eiffel-1.png', grey=True)

hf = view1.Harris(nfeat=150)
view1.disp(grid=True, darken=True, title=False)
hf.plot()
rvcprint.rvcprint(subfig='a')

plt.clf()
view1.disp(grid=True, darken=True, title=False)
sf = view1.SIFT().sort().filter(minscale=10)[:150]
sf.plot(filled=True, color='y', alpha=0.3)
rvcprint.rvcprint(subfig='b')
