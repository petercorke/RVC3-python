#!/usr/bin/env python3

import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath import *
import matplotlib.pyplot as plt
import numpy as np

p560 = models.DH.Puma560()

TE1 = SE3(0.4, -0.2, 0.6) * SE3.Rx(3);
TE2 = SE3(0.4, 0.2, 0.6) * SE3.Rx(1);
t = np.arange(0, 2, 0.02)

Ts = ctraj(TE1, TE2, t)

sol = p560.ikine_a(Ts, 'ru')
qc = sol.q

xplot(t, qc, wrist=True)

rvcprint.rvcprint(subfig='a', thicken=1.5)

plt.clf()
plt.plot(t, Ts.t)
p = Ts.t
plt.ylabel('Position (m)')
plt.xlabel('Time (s)')
plt.legend(['x', 'y', 'z'])
plt.legend(['x', 'y', 'z'], loc='lower right');
plt.xlim(0, 2)

rvcprint.rvcprint(subfig='b', thicken=1.5)

p = Ts.t
plt.clf()
plt.plot(p[:,0], p[:,1])
plt.xlabel('x (m)')
plt.ylabel('y (m)');
plt.plot(p[0,0], p[0,1], 'o', markerfacecolor='k', markersize=7, markeredgecolor='None')
plt.plot(p[-1,0], p[-1,1], '*', markerfacecolor='k', markersize=12, markeredgecolor='None')
plt.ylim(-0.21, 0.21)
# plt.axis equal

rvcprint.rvcprint(subfig='c', thicken=1.5)

plt.clf()
plt.plot(t, Ts.rpy('xyz'))
plt.ylabel('RPY angles (rad)')
plt.xlabel('Time (s)')
plt.legend(['roll', 'pitch', 'yaw'], loc='upper right');
plt.xlim(0, 2)

rvcprint.rvcprint(subfig='d', thicken=1.5)
