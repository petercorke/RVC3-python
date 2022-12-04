#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from math import pi
from spatialmath import SE3
from spatialmath.base import e2h, h2e, plot_sphere, homtrans
import math


P = np.array([
    [-1, -1, 2, 2],
    [1, 2, 2, 1],
    [0, 0, 0, 0]
])

camera = CentralCamera(f=0.012, rho=10e-6, imagesize=1000, 
        pose=SE3(0, 0, 8) * SE3.Rx(-2.8))
print(camera)

print(camera.project_point(P))

C = camera.C()
H = np.delete(C, 2, axis=1)
print(H)

print(h2e(H @ e2h(P[:2, :])))
print(homtrans(H, P[:2, :]))

p = np.array([
    [0, 0, 1000, 1000],
    [0, 1000, 1000, 0]
])

Pp = h2e(np.linalg.inv(H) @ e2h(p))
print(P)

camera.plot(scale=2, shape='camera', color='k', frame=True)
plot_sphere(radius=0.1, centre=P, color='r')
# plot_sphere(radius=0.1, centre=np.vstack((Pp, np.zeros((4,)))), color='b')
corners = np.vstack((Pp, np.zeros((4,))))
for i in range(4):
    j = (i + 1) % 4
    p1 = corners[:,i]
    p2 = corners[:,j]
    if i == 0:
        label = 'Camera FOV'
    else:
        label = ''
    plt.plot((p1[0], p2[0]), (p1[1], p2[1]), (p1[2], p2[2]), 'b--', label=label)

ax = plt.gca()
ax.set_xlim(-8, 12)
ax.set_ylim(-10, 10)
ax.set_zlim(0, 10)
ax.legend()


rvcprint.rvcprint(interval=4)