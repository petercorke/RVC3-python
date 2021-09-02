#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)

disparity = L.StereoSGBM(R, 2, [40, 90], (4, 100))
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='a')

disparity = L.StereoBM(R, 3, [40, 90], (4, 100))
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='b')

disparity = L.StereoBM(R, 5, [40, 90], (4, 100))
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='c')

disparity = L.StereoBM(R, 11, [40, 90])
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='d')

