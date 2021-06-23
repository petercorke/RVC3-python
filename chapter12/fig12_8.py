#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('multiblobs.png')
im.disp(title=False, black=0.3)
rvcprint.rvcprint(subfig='a')

blobs = im.blobs()

labels = blobs.labelImage(image=im)

labels.disp(colormap='viridis', ncolors=len(blobs), colorbar=True)
rvcprint.rvcprint(subfig='b')

reg5 = labels == 5
reg5.disp(black=0.3)
rvcprint.rvcprint(subfig='c')

