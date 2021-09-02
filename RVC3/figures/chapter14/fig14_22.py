#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, *_ = L.DSI(R, 3, [40, 90])

disparity.disp(grid=True, badcolor='red', colorbar=dict(label='Disparity (pixels)'))

rvcprint.rvcprint(debug=True)
