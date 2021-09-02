#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from machinevisiontoolbox.base.imageio import convert


dartmouth = WebCam('https://webcam.dartmouth.edu/webcam/image.jpg')

dartmouth.grab().disp()

# commented out so we don't auto clobber a nice image
# rvcprint.rvcprint()

# for im in dartmouth:

#     plt.imshow(im.image)
#     plt.pause(0.02)