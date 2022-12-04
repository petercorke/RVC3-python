#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im1 = Image.Read('eiffel-1.png')
im1.disp(grid=True)
rvcprint.rvcprint(subfig='a')

im2 = Image.Read('eiffel-2.png')
im2.disp(grid=True)
rvcprint.rvcprint(subfig='b')
