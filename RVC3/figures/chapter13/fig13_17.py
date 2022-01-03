#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3


camera = FishEyeCamera(
            projection='equiangular',
            rho=10e-6,
            imagesize=[1280, 1024]
            )

X, Y, Z = mkcube(0.2, centre=[0.2, 0, 0.3], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


rvcprint.rvcprint(facecolor=None)

