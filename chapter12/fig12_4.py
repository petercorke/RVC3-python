#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

castle = Image.Read('castle2.png', dtype='float')

t = castle.adaptive_thresh(width=30).disp()
rvcprint.rvcprint(subfig='a')

