#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from math import pi

camera = CatadioptricCamera(
            projection='equiangular',
            rho=10e-6,
            imagesize=[1280, 1024],
            maxangle=pi/4
        )
     
X, Y, Z = mkcube(1, centre=[1, 1, 0.8], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


rvcprint.rvcprint(facecolor=None)
