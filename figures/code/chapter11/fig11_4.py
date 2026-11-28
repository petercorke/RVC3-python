#!/usr/bin/env python3

from RVC3.tools import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from machinevisiontoolbox.base.imageio import convert


# the Dartmouth webcam used in the first edition no longer responds, so use a
# camera in Porjus, Lappland, Sweden (as the chapter 11 notebook does)
porjus = WebCam('http://uk.jokkmokk.jp/photo/nr4/latest.jpg')

next(porjus).disp()

# commented out so we don't auto clobber a nice image
# rvcprint.rvcprint()

# for im in porjus:

#     plt.imshow(im.image)
#     plt.pause(0.02)