#!/usr/bin/env python3

import numpy as np
import scipy as sp

def ransac_line(x, y, npoints=2, maxiter=20, t=1e-6, d=4):

    iterations = 0
    n = len(x)
    best_fit = np.inf
    best_model = None

    while True:
        inliers = list(np.random.choice(np.arange(len(x)), npoints, replace=False))

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

if __name__ == "__main__":
    # import rvcprint

    import matplotlib.pyplot as plt
    from machinevisiontoolbox import *


    n = 11
    nbad = 4

    x = np.arange(n)
    y = 3 * x - 10

    plt.plot(x,y, 'k', label='_nolegend_')
    plt.grid(True)


    np.random.seed(1)
    bad = np.random.choice(n, nbad, replace=False)
    print(bad)
    good = list(set(np.arange(11)) - set(bad))
    y[bad] = y[bad] + np.random.rand(nbad) * 10 + 2
    plt.plot(x[good], y[good], 'ko', markerfacecolor='k', markersize=8)
    plt.plot(x[bad], y[bad], 'ro', markerfacecolor='r', markersize=8)

    m, c, *_ = sp.stats.linregress(x, y)

    plt.plot(x, m * x + c, 'r--')

    th, inliers = ransac_line(x, y)
    print(inliers)

    plt.plot(x, th[0] * x + th[1], 'bs-', markerfacecolor='w', markersize=3)

    # grid
    plt.ylabel('$y = 3x-10$')
    plt.xlabel('$x$')
    plt.xlim(-0.5, 10.1)
    plt.ylim(-10.5, 30)
    plt.legend(['good data point', 'bad data point', 'least squares estimate', 'RANSAC estimate'])

    # rvcprint.rvcprint()


