#!/usr/bin/env python3


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('sharks.png')
im.disp(title=False, black=0.1)
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

labels, nblobs = im.labels_binary()
labels.disp(colormap='viridis', ncolors=nblobs, colorbar=dict(shrink=0.8, aspect=20*0.8))


rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

reg2 = labels == 3
reg2.disp(black=0.1)
rvcprint.rvcprint(subfig='c')

# blobs = im.blobs()
# labels = blobs.labelImage(image=im)
# labels.disp(colormap='viridis', ncolors=len(blobs), colorbar=dict(shrink=0.8, aspect=20*0.8))

# rvcprint.rvcprint(subfig='d')
