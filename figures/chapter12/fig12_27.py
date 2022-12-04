#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# def scalespace(im, n, sigma=1):

#     g = [im]
#     scale = 0.5
#     scales = [scale]
#     lap = []

#     for i in range(n-1):
#         im = im.smooth(sigma)
#         scale = np.sqrt(scale ** 2 + sigma ** 2)
#         scales.append(scale)
#         g.append(im)
#         x = (g[-1] - g[-2]) * scale ** 2 
#         lap.append(x)

#     return g, lap, scales


def scaleplot(k):
    L[k].disp(colormap='signed', square=True, grid=True)
    plt.text(10, 180, f"$\sigma$ = {s[k]:.3g}")
    plt.plot(63, 63, 'k+')
    plt.plot(127, 63, 'k+')
    plt.plot(63, 127, 'k+')
    plt.plot(127, 127, 'k+')

im = Image.Read('scale-space.png', dtype='float')
im.disp(square=True, black=0.3, grid=True)
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

G, L, s = im.scalespace(60, sigma=2)
scaleplot(5)
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

scaleplot(20)
rvcprint.rvcprint(subfig='c')

# ----------------------------------------------------------------------- #

scaleplot(35)
rvcprint.rvcprint(subfig='d')

# ----------------------------------------------------------------------- #

scaleplot(55)
rvcprint.rvcprint(subfig='e')

# ----------------------------------------------------------------------- #

plt.clf()
plt.plot(s[:-1], [-M.image[63, 63] for M in L])
plt.plot(s[:-1], [-M.image[63, 127] for M in L])
plt.plot(s[:-1], [-M.image[127, 63] for M in L])
plt.plot(s[:-1], [-M.image[127, 127] for M in L])
plt.xlim(0, s[-1])
plt.ylim(0, 2)
plt.grid(True)
plt.xlabel('Scale')
plt.ylabel('$\|$LoG$\|$')
plt.legend(['5x5', '9x9', '17x17', '33x33'])

rvcprint.rvcprint(subfig='f')




