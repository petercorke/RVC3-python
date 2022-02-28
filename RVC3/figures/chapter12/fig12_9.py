#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

castle = Image.Read('castle2.png')

mser, nregions = castle.labels_MSER()
print(nregions)
# mser.hist().plot()
mser.disp(colormap='viridis_r', colorbar=dict(shrink=0.8, aspect=20*0.8))

rvcprint.rvcprint()

