#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

sharks = Image.Read('sharks.png')

sharks.disp(black=0.3)

fv = sharks.blobs()
print(fv)

fv.plot_centroid()
fv.plot_contour()

rvcprint.rvcprint()
