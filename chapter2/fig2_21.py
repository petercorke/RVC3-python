import rvcprint
from math import pi
from spatialmath.base import *
from spatialmath import Twist3
import matplotlib.pyplot as plt
import numpy as np

X = transl(3, 4, -4)

tw = Twist3.Revolute([0, 0, 1], [2, 3, 2], 0.5)

angles = np.arange(0, 15, 0.3)
plotvol3([0, 5, 0, 5, -5, 5], grid=True)
trplot([tw.exp(theta).A @ X for theta in angles], length=(0.5, 0.5, 1), style='line', color='rgb', width=2, origindot=5.0)

L = tw.line()
L.plot('k:', linewidth=2)

rvcprint.rvcprint()