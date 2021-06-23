#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

def scalespace(im, n, sigma=1):

    g = [im]
    scale = 0.5
    scales = [scale]
    lap = []

    for i in range(n-1):
        im = im.smooth(sigma)
        scale = np.sqrt(scale ** 2 + sigma ** 2)
        scales.append(scale)
        g.append(im)
        x = (g[-1] - g[-2]) * scale ** 2 
        lap.append(x)

    return g, lap, scales

mona = Image.Read('monalisa.png', grey=True, dtype='float')
G, L, s = scalespace(mona, 8, 8)
Image.Tile([G]).disp(width=500)
rvcprint.rvcprint(subfig='a')

Image.Tile([L]).disp(width=500, colormap='signed')
rvcprint.rvcprint(subfig='b')
