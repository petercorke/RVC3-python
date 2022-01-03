#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)


disparity = L.stereo_BM(R, 3, [40, 90])
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='a')
#----------------------------------------------------------------------- #

disparity = L.stereo_BM(R, 3, [40, 90], (200, 2))
disparity.disp(grid=True)

rvcprint.rvcprint(subfig='b')
#----------------------------------------------------------------------- #

disparity = L.stereo_BM(R, 5, [40, 90], (200, 2))
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='c')
#----------------------------------------------------------------------- #

disparity = L.stereo_BM(R, 11, [40, 90])
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='d')
#----------------------------------------------------------------------- #

disparity = L.stereo_SGBM(R, 3, [40, 90], (200, 2))
disparity.disp(grid=True)
rvcprint.rvcprint(subfig='e')


