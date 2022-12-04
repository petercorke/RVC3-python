#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from math import pi

camera = SphericalCamera()
print(camera)

X, Y, Z = mkcube(1, centre=[2, 3, 1], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


rvcprint.rvcprint(facecolor=None)

