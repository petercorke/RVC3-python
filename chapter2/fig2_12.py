import rvcprint
from math import pi
from spatialmath.base import *
import matplotlib.pyplot as plt
import numpy as np

plotvol2([-5, 4, -1, 4.5], grid=True)
T0 = np.eye(3,3)
trplot2(T0, frame='0')
X = transl2(2, 3)
trplot2(X, frame='X')

R = trot2(2)

trplot2(R @ X, framelabel='RX', color='r')
trplot2(X @ R, framelabel='XR', color='r')

C = np.r_[1, 2]
plot_point(C, 'ko', label='C', textcolor='k', fillcolor='k')


RC = transl2(C) @ R @ transl2(-C)
trplot2(RC @ X, framelabel='XC', color='r')

rvcprint.rvcprint()