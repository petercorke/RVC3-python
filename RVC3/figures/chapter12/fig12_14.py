#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import base
import os


im = Image.Read('multiblobs.png')
blobs = im.blobs()

dotfile = rvcprint.figname() + '.dot'
blobs.dotfile(dotfile)
os.system("dot -Tpdf -o {} {}".format(rvcprint.outfile(format='pdf'), dotfile))
