#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('58060.png')
im.disp(title=False)
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

labels, n = im.labels_graphseg()
print(n)

labels.disp(colormap='viridis_r', ncolors=n, colorbar=dict(shrink=0.7, aspect=20*0.7))
rvcprint.rvcprint(subfig='b')

