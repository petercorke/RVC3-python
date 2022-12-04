#!/usr/bin/env python3

from roboticstoolbox import *
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3
from math import pi
import rvcprint
from mpl_toolkits.mplot3d import Axes3D, proj3d


# Copyright (C) 1993-2021, by Peter I. Corke


mm = 0.001   
L1 = 100 * mm
L2 = 100 * mm

# leg.plot([0,0,0], block=True, eeframe=False, jointaxes=False, backend='pyplot', shadow=False)

# define the key parameters of the gait trajectory, walking in the
# x-direction
xf = 50; xb = -xf;   # forward and backward limits for foot on ground
y = -50;              # distance of foot from body along y-axis
zu = -20; zd = -50;     # height of foot when up and down
# define the rectangular path taken by the foot
segments = np.array([
    [xf, y, zd],
    [xb, y, zd],
    [xb, y, zu],
    [xf, y, zu],
    [xf, y, zd]
     ]) * mm

# build the gait. the points are:
#   1 start of walking stroke
#   2 end of walking stroke
#   3 end of foot raise
#   4 foot raised and forward
#
# The segments times are :
#   1->2  3s
#   2->3  0.5s
#   3->4  1s
#   4->1  0.5ss
#
# A total of 4s, of which 3s is walking and 1s is reset.  At 0.01s sample
# time this is exactly 400 steps long.
#
# We use a finite acceleration time to get a nice smooth path, which means
# that the foot never actually goes through any of these points.  This
# makes setting the initial robot pose and velocity difficult.
#
# Intead we create a longer cyclic path: 1, 2, 3, 4, 1, 2, 3, 4. The
# first 1->2 segment includes the initial ramp up, and the final 3->4
# has the slow down.  However the middle 2->3->4->1 is smooth cyclic
# motion so we "cut it out" and use it.
print('create trajectory\n')

x = mstraj(segments, tsegment=[3, 0.25, 0.5, 0.25], dt=0.01, tacc=0.07)
print(x.q.shape)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(x.t[:300], x.q[:300,0]/mm, x.q[:300,2]/mm, color='black', label='stance phase')
plt.plot(x.t[299:], x.q[299:,0]/mm, x.q[299:,2]/mm, color='red', label='reset phase')

print(x.q.shape)
ax.view_init(10, -82)

plt.xlabel('Time (s)')
plt.ylabel('x (mm)')
ax.set_zlabel('z (mm)')
f = lambda x,y,z: proj3d.proj_transform(x,y,z, ax.get_proj())[:2]
ax.legend(loc="lower left", bbox_to_anchor=f(0., 40, -30), 
          bbox_transform=ax.transData)
# plt.show(block=True)

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.clf()
x = x.q[:, 0]
# HACK
x = np.r_[x, 0, 0, 0]
for i in range(4):
    t = np.arange(0, 4, 0.01)
    q = [x[(i * 100 + j) % 400]/mm for j in range(400)]
    plt.plot(t, q)


plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('Foot x-coordinate (mm)')
plt.legend(['Foot 0', 'Foot 1', 'Foot 2', 'Foot 3'], loc='lower right')

# rvcprint('subfig', 'b', 'thicken', 1.5)
rvcprint.rvcprint(subfig='b')
