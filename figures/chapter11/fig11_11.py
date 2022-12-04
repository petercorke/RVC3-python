#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm

foreground = Image.Read('greenscreen.png', dtype='float')

foreground.disp(title=False)
rvcprint.rvcprint(subfig='a')

cc = foreground.gamma_decode('sRGB').tristim2cc()
print(cc)
h = cc.plane('g').hist()

plt.clf()
h.plot()
plt.xlabel('Chromaticity (g)');
plt.grid(True)
ylim = plt.gca().get_ylim()
plt.plot([0.45, 0.45], ylim, 'b--')
rvcprint.rvcprint(subfig='b')

mask = cc.plane('g') < 0.45
mask.disp(black=0.2)
rvcprint.rvcprint(subfig='c')

mask3 = mask.colorize()
(foreground * mask3).disp()
rvcprint.rvcprint(subfig='d')

background = Image.Read('road.png', dtype='float').samesize(foreground)
(background * (1 - mask3)).disp()
rvcprint.rvcprint(subfig='e')

(foreground * mask3  + background * (1 - mask3)).disp()
rvcprint.rvcprint(subfig='f')
