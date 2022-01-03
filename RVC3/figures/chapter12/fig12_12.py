#!/usr/bin/env python3


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = Image.Read('sharks.png')
im.disp()

blobs = im.blobs()
blobs.plot_centroid()
blobs.plot_box(color='r')
rvcprint.rvcprint(subfig='a')
# ----------------------------------------------------------------------- #

im.roi(blobs[1].bbox).rotate(blobs[1].orientation).disp()
rvcprint.rvcprint(subfig='b')
