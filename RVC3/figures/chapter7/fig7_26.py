#!/usr/bin/env python3

from roboticstoolbox import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
from spatialmath import SE3
from spatialgeometry import Cuboid
from math import pi
import rvcprint

# Copyright (C) 1993-2021, by Peter I. Corke


mm = 0.001   
L1 = 100 * mm
L2 = 100 * mm


print('create leg model\n')

# now create a robot to represent a single leg
leg = ERobot(ETS.rz() * ETS.rx() * ETS.ty(L1) * ETS.rx() * ETS.tz(-L2))
print(leg)

# leg.plot([0,0,0], block=True, eeframe=False, jointaxes=False, backend='pyplot', shadow=False)

# define the key parameters of the gait trajectory, walking in the
# x-direction
xf = 50; xb = -xf;   # forward and backward limits for foot on ground
y = -50;              # distance of foot from body along y-axis
zu = -20; zd = -50;     # height of foot when up and down
# define the closed rectangular path taken by the foot
via = np.array([
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
# The segment times are :
#   1->2  3s
#   2->3  0.5s
#   3->4  1s
#   4->1  0.5s
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

x = mstraj(via, tsegment=[3, 0.25, 0.5, 0.25], dt=0.01, tacc=0.1)

print('inverse kinematics (this will take a moment)...')
xcycle = x.q
xcycle = np.vstack((xcycle, xcycle[-3:,:]))

sol = leg.ikine_LM(SE3(xcycle), mask=[1, 1, 1, 0, 0, 0])
qcycle = sol.q

print(xcycle.shape)

# dimensions of the robot's rectangular body, width and height, the legs
# are at each corner.
W = 100 * mm; L = 200 * mm

# create 4 leg robots.  Each is a clone of the leg robot we built above,
# has a unique name, and a base transform to represent it's position
# on the body of the walking robot.
legs = [
    ERobot(leg, name='leg0', base=SE3( L / 2, -W / 2, 0)),
    ERobot(leg, name='leg1', base=SE3(-L / 2, -W / 2, 0)),
    ERobot(leg, name='leg2', base=SE3( L / 2,  W / 2, 0) * SE3.Rz(pi)),
    ERobot(leg, name='leg3', base=SE3(-L / 2,  W / 2, 0) * SE3.Rz(pi))
]

from roboticstoolbox.backends.PyPlot import PyPlot

env = PyPlot()
env.launch(limits=[-L, L, -W, W, -0.15, 0.05])

# instantiate each robot in the backend environment
for leg in legs:
    leg.q = np.r_[0, 0, 0]
    env.add(leg, readonly=True, jointaxes=False, eeframe=False, shadow=False)
body = Cuboid([L, W, 30 * mm], color='b')
env.add(body)
env.step()

def gait(cycle, k, offset, flip):
    k = (k + offset) % cycle.shape[0]
    q = cycle[k, :]
    if flip:
        q[0] = -q[0]   # for left-side legs
    return q

env.step()

# walk!


for i in range(50):
    legs[0].q = gait(qcycle, i, 0, False)
    legs[1].q = gait(qcycle, i, 100, False)
    legs[2].q = gait(qcycle, i, 200, True)
    legs[3].q = gait(qcycle, i, 300, True)
    env.step(dt=0.02)

rvcprint.rvcprint(thicken=2, interval=0.05)