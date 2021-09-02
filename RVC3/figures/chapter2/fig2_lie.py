#! /usr/bin/env python3
from spatialmath import SO3, base
import numpy as np
import matplotlib.pyplot as plt
import rvcprint

# base.plotvol3(2)
SO3().plot(frame='O', colors=('r', 'g', 'b'), projection='persp')

points = np.array([[-1, 1, 1, -1, -1], [1, 1, -1, -1, 1], [0,0,0,0,0]])

d = [-1, -1, 1.8]

R = SO3.OA([0,1,0], d)

xyz = R * points
plt.plot(xyz[0,:], xyz[1,:], xyz[2,:], '-o')

R.plot(frame='r')

c = base.circle(centre=(0,0,0))
c = np.array([c[0], c[1], 0*c[0]])
xyz = R * c
plt.plot(xyz[0,:], xyz[1,:], xyz[2,:], '-r')

rvcprint.rvcprint()