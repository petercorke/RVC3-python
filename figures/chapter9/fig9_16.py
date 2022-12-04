#!/usr/bin/env python3

import matplotlib.pyplot as plt
import rvcprint
import numpy as np
from math import pi
from roboticstoolbox import *

puma = models.DH.Puma560()

N = 100
(Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
M00 = np.zeros((N,N))
M01 = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        M = puma.inertia(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
        M00[i,j] = M[0,0]
        M01[i,j] = M[0,1]
plt.axes(projection="3d").plot_surface(Q2, Q3, M00)
plt.xlabel('$\mathbf{q_1}$ (rad)')
plt.ylabel('$\mathbf{q_2}$ (rad)')
plt.gca().set_zlabel(r'$\mathbf{m_{00}} \mathrm{(kg\,m^2)}$')
plt.grid(True)


rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
plt.axes(projection="3d").plot_surface(Q2, Q3, M01)
plt.xlabel('$\mathbf{q_1}$ (rad)')
plt.ylabel('$\mathbf{q_2}$ (rad)')
plt.gca().set_zlabel(r'$\mathbf{m_{01}} \mathrm{(kg\,m^2)}$')
plt.grid(True)
rvcprint.rvcprint(subfig='b')

# ------------------------------------------------------------------------- #

q2 = np.linspace(-pi, pi, N)
M11 = np.zeros((N,))
for i in range(N):
    M = puma.inertia(np.r_[0, 0, q2[i], 0, 0, 0])
    M11[i] = M[1, 1]

plt.clf()
plt.plot(q2, M11)
plt.xlabel('$\mathbf{q_2}$ (rad)')
plt.ylabel('$\mathbf{m_{11}} \mathrm{(kg\,m^2)}$')
plt.grid(True)
rvcprint.rvcprint(subfig='c')