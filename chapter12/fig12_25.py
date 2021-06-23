#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import scipy as sp
import spatialmath.base as smb

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

def scalemax(L, scale):

    # absolute value of Laplacian as a 3D matrix, with scale along axis 2
    L = np.dstack([np.abs(x.image) for x in L])

    # find maxima within all 26 neighbouring pixels
    # create 3x3x3 structuring element and maximum filter
    se_nhood = np.ones((3,3,3))
    se_nhood[1, 1, 1] = 0
    eps = np.finfo(np.float64).eps
    maxima = (L > sp.ndimage.maximum_filter(L, footprint=se_nhood, mode='nearest')) & (L > 100 * eps)

    # find the locations of the minima
    i, j, k = np.nonzero(maxima)
    
    # create result matrix, one row per feature: i, j, k, |L|
    # where k is index into scale
    result = np.column_stack((j, i, np.r_[scale][k], L[i, j, k]))

    # sort the rows on strength column, descending order
    k = np.argsort(-result[:, 3])
    return result[k, :]


im = Image.Read('scale-space.png', dtype='float')
im.disp(square=True, black=0.3, grid=True, title=False)

G, L, s = scalespace(im, 60, 2)

features = scalemax(L, s)
print(features)

for feature in features:
    plt.plot(feature[0], feature[1], 'k+')
    smb.plot_circle(feature[2] * np.sqrt(2), 'y', centre=feature[:2])

rvcprint.rvcprint()

# plt.show(block=True)