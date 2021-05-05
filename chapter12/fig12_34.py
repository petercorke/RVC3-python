#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm

roof = Image.Read('roof.png', grey=True)

roof.disp(title=False)
rvcprint.rvcprint(subfig='a')

smaller = roof.image[0::7, 0::7]
idisp(smaller)
rvcprint.rvcprint(subfig='b')

smaller = roof.scale(1 / 7, sigma=3)
smaller.disp()
rvcprint.rvcprint(subfig='c')

bigger = smaller.scale(7)
bigger.disp()
rvcprint.rvcprint(subfig='d')
