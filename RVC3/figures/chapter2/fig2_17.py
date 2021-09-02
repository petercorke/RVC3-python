#! /usr/bin/env python3
import rvcprint
from math import pi
from spatialmath.base import *
import matplotlib.pyplot as plt
import numpy as np


plotvol3(1, grid=True)
R = rotx(pi/2)
trplot(R)

rvcprint.rvcprint(subfig='a', interval=0.5)

plotvol3(1, grid=True)
R = rotx(pi/2) @ roty(pi/2)
plt.clf()
plotvol3(1, grid=True)
trplot(R)

# plt.show(block=True)
rvcprint.rvcprint(subfig='b', interval=0.5)
