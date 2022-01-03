#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm


mona = Image.Read('monalisa.png', grey=True, dtype='float')

np.random.seed(0)  # reset random numbers

spotty = mona.view1d()
npix = mona.npixels
k = np.random.choice(npix, (5000,), replace=False)
spotty[k[:5000]] = 0
spotty[k[5000:]] = 1

mona.disp(title=False, grid='y', interpolation='nearest')
rvcprint.rvcprint(subfig='a')

mona.rank(np.ones((3,3)), rank=4).disp(grid='y')
rvcprint.rvcprint(subfig='b')

