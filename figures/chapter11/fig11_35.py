#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm

roof = Image.Read('roof.png', grey=True)

roof.disp(title=False)
rvcprint.rvcprint(subfig='a')

smaller = roof[::7, ::7]
smaller.disp()
rvcprint.rvcprint(subfig='b')

smaller = roof.smooth(sigma=3)[::7, ::7]
smaller.disp()
rvcprint.rvcprint(subfig='c')

bigger = smaller.replicate(7)
bigger.disp()
rvcprint.rvcprint(subfig='d')
