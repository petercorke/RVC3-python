#!/usr/bin/env python3

import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt
import rvcprint
from spatialmath.base import *

E = np.array([[1, 1], [1, 2]]);


# generate a set of points within the ellipse
rng = np.random.default_rng(0)
x = []
while len(x) < 200:
	p = rng.uniform(low=-2, high=2, size=(2,1))
	if np.linalg.norm(p.T @ E @ p) <= 1:
		x.append(p)
x = np.hstack(x)  # 2 x 50 array
plt.plot(x[0, :], x[1, :], "k.")

# compute the moments
m00 = mpq_point(x, 0, 0)
m10 = mpq_point(x, 1, 0)
m01 = mpq_point(x, 0, 1)
xc = np.c_[m10, m01] / m00

#  compute second moments relative to centroid (central moments)
x0 = x - xc.T;
u20 = mpq_point(x0, 2, 0);
u02 = mpq_point(x0, 0, 2);
u11 = mpq_point(x0, 1, 1);

# compute the moments and ellipse matrix
J = np.array([[u20, u11], [u11, u02]]);
E_est = m00 / 4 * np.linalg.inv(J)
plot_ellipse(E_est, "r")

plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.gca().set_aspect('equal')
plt.legend(['data points', 'fitted ellipse'])
rvcprint.rvcprint()
