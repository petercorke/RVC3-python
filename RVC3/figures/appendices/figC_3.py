#!/usr/bin/env python3

import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt
import rvcprint
from spatialmath.base import *

E = np.array([[1, 1], [1, 2]]);


th = np.linspace(0, 2*np.pi, 50);
y = np.vstack([np.cos(th), np.sin(th)]);
plt.plot(y[0, :], y[1, :], 'r--');

x = np.linalg.inv(scipy.linalg.sqrtm(E)) @ y;
plt.plot(x[0, :], x[1, :], 'b');

e, v = np.linalg.eig(E)
r = 1 / np.sqrt(e)
plot_arrow((0, 0), v[:,0]*r[0], color="r", width=0.02);
plot_arrow((0, 0), v[:,1]*r[1], color="b", width=0.02);

plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.gca().set_aspect('equal')

plt.legend(['unit circle', 'ellipse', 'major axis', 'minor axis'], loc='upper right')
rvcprint.rvcprint()
