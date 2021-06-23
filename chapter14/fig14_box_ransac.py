#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import scipy as sp

def ransac(x, y, npoints=2, maxiter=20, t=1e-6, d=4):

    iterations = 0
    n = len(x)
    best_fit = np.inf
    best_model = None

    while True:
        inliers = list(np.random.randint(0, len(x), npoints))

        m, c, r2, *_ = sp.stats.linregress(x[inliers], y[inliers])
        new_inliers = []
        for k in range(len(x)):
            if k in inliers:
                continue
            if np.linalg.norm(m * x[k] + c - y[k]) < t:
                new_inliers.append(k)

        inliers.extend(new_inliers)
        if len(inliers) >= d:
            # decent model
            m, c, r2, *_ = sp.stats.linregress(x[inliers], y[inliers])
            err = np.linalg.norm(m * x[inliers] + c - y[inliers])
            if err < best_fit:
                best_fit = err
                best_model = (m, c)
                best_inliers = inliers

        iterations += 1
        if iterations > maxiter:
            break
    
    return best_model, best_inliers


x = np.linspace(0, 10, 10)
y = 3 * x - 10

plt.plot(x,y, 'k', label='_nolegend_')
plt.grid(True)


np.random.seed(0)

k = np.random.randint(1, len(x)-1, (5,))
good = np.ones((len(x),), np.bool)
good[k] = False
y[~good] = y[~good] + np.random.rand(len(k)) * 10
plt.plot(x[good], y[good], 'ko', markerfacecolor='k', markersize=8)
plt.plot(x[~good], y[~good], 'ro', markerfacecolor='r', markersize=8)

m, c, *_ = sp.stats.linregress(x, y)

plt.plot(x, m * x + c, 'b--')

th, inliers = ransac(x, y)

plt.plot(x, th[0] * x + th[1], 'bs', markerfacecolor='w', markersize=3)

# grid
plt.ylabel('$y = 3x-10$')
plt.xlabel('$x$')
plt.xlim(-0.5, 10.1)
plt.ylim(-10.5, 25)
plt.legend(['good data point', 'bad data point', 'least squares estimate', 'RANSAC estimate'])

rvcprint.rvcprint()
# plt.show(block=True)


