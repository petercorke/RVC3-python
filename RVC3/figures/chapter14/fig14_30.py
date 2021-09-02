#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

[di,sim,peak] = istereo(L, R, [40 90], 3, 'interp')

di(isnan(di)) = Inf
idisp(di, 'nogui')
c=colormap
c=[c 1 0 0]
colormap(c)
h = colorbar
h.Label.String = 'Disparity (pixels)'
h.Label.FontSize = 10

rvcprint.rvcprint(subfig='a', 'svg')

A = peak.A
A(isnan(A)) = Inf
idisp(abs(A), 'nogui')
c=colormap
c=[c 1 0 0]
colormap(c)
h = colorbar
h.Label.String = '|A| (peak sharpness)'
h.Label.FontSize = 10

rvcprint.rvcprint(subfig='b', 'svg')
