#! /usr/bin/env python3
from roboticstoolbox import *
from spatialmath import *
import numpy as np
from math import pi
import matplotlib.pyplot as plt

np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})
dt = 0.05

puma = models.DH.Puma560()

r = 0.05
Tc = 5
cc = puma.fkine(puma.qn).t
def circle(t):
    x = r * np.cos(t / Tc * 2 * pi) + cc[0]
    y = r * np.sin(t / Tc * 2 * pi) + cc[1]
    return SE3(x, y, cc[2]) * SE3.OA([0,1,0], [1,0,0])

q = [0, pi/4, pi, 0, pi/4, 0]

q = puma.qn


xyz = np.empty((0, 3))
for t in np.arange(0, 5, dt):

    T = circle(t)
    Tfk = puma.fkine(q)

    J = puma.jacobe(q)

    delta = base.tr2delta(Tfk.A, T.A)
    dq = 5 * np.linalg.inv(J) @ delta
    print(np.linalg.det(J), base.norm(delta), delta)
    print('dq', dq)
    print()
    # print(q)
    q = q +  dq * dt


    xyz = np.vstack((xyz, Tfk.t))

plt.figure()
plt.plot(xyz[:,0], xyz[:,1])
plt.show(block=True)