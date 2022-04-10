#! /usr/bin/env python3
import rvcprint
from math import pi
from spatialmath.base import *
import matplotlib.pyplot as plt
import numpy as np

plotvol2([-5, 4, -1, 4.5], grid=True)
T_0 = np.eye(3,3)
trplot2(T_0, frame='0', color='k', axissubscript=False)
T_X = transl2(2, 3)
trplot2(T_X, frame='X', color='b', axissubscript=False)

T_R = trot2(2)

trplot2(T_R @ T_X, frame='RX', axissubscript=False, color='g')
trplot2(T_X @ T_R, frame='XR', axissubscript=False, color='g')

C = np.r_[3, 2]
plot_point(C, 'ko', text=' C', color='k')


T_C = transl2(C) @ T_R @ transl2(-C)
print(trlog2(T_C))
trplot2(T_C @ T_X, frame='XC', axissubscript=False, color='r')

plot_circle(np.sqrt(2), C, 'k:', zorder=0)
plot_circle(np.sqrt(13), (0, 0), 'k--', zorder=0)

rvcprint.rvcprint()