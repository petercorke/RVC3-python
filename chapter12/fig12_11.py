#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

sharks = Image.Read('sharks.png')
sharks.disp(title=False, black=0.3)
rvcprint.rvcprint(subfig='a')

labels, n = sharks.labels_binary()
blob = labels == 3

blob.disp(black=0.3, grid=True)
rvcprint.rvcprint(subfig='b')

uv = blob.nonzero()

umin = uv[0, :].min()
umax = uv[0, :].max()
vmin = uv[1, :].min()
vmax = uv[1, :].max()
# print(umin, umax, vmin, vmax)

# print(blob.moments())

