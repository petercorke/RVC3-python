#!/usr/bin/env python3

import matplotlib.pyplot as plt
import rvcprint
import numpy as np
from math import pi
from roboticstoolbox import *

puma = models.DH.Puma560()

N = 100
(Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
g1 = np.zeros((N,N))
g2 = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        g = puma.gravload(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
        g1[i,j] = g[1]  # shoulder gravity load
        g2[i,j] = g[2]  # elbow gravity load
plt.axes(projection="3d").plot_surface(Q2, Q3, g1)
plt.xlabel('$\mathbf{q_1}$ (rad)')
plt.ylabel('$\mathbf{q_2}$ (rad)')
plt.gca().set_zlabel('$\mathbf{g_1}$ (Nm)')
plt.grid(True)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
plt.axes(projection="3d").plot_surface(Q2, Q3, g2)
plt.xlabel('$\mathbf{q_1}$ (rad)')
plt.ylabel('$\mathbf{q_2}$ (rad)')
plt.gca().set_zlabel('$\mathbf{g_2}$ (Nm)')
plt.grid(True)
rvcprint.rvcprint(subfig='b')
