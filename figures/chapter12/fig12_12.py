#!/usr/bin/env python3


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath.base import plot_point

im = Image.Read('sharks.png')
im.disp()

blobs = im.blobs()
blobs.plot_centroid(marker='+', color='blue')
blobs.plot_box(color='r')
plot_point(blobs.p, marker='None', text="#{0}")
rvcprint.rvcprint(subfig='a')
# ----------------------------------------------------------------------- #

im.roi(blobs[1].bbox).rotate(blobs[1].orientation).disp()
rvcprint.rvcprint(subfig='b')
