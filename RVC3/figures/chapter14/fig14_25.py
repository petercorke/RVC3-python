#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)
3
disparity, *_ = L.stereo_simple(R, 3, [40, 90])

disparity.disp(grid=True, badcolor='red', colorbar=dict(shrink=0.92, aspect=20*0.92, label='Disparity (pixels)'))

rvcprint.rvcprint()
