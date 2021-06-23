#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

import runpy

globals = runpy.run_module('fig13_6', init_globals={'_rvcprint': False})
image = globals['targets_binary']
blobs = image.blobs()
labels = blobs.labelImage(image=image)
labels.disp(ncolors=len(blobs), colormap='jet', colorbar=True)
rvcprint.rvcprint(subfig='a')

globals = runpy.run_module('fig13_7', init_globals={'_rvcprint': False})

image = globals['tomatoes_binary']
blobs = image.blobs()
labels = blobs.labelImage(image=image)
labels.disp(ncolors=len(blobs), colormap='jet', colorbar=True)
rvcprint.rvcprint(subfig='b')

