#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath import SE3
from spatialmath.base import plotvol3, plot_sphere

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera(name='camera 1', f=0.002, pose=T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera(name='camera 2', f=0.002, pose=T2)

ax = plotvol3([-0.4, 0.6, -0.5, 0.5, -0.2, 1])

# cam1.plot_camera(ax=ax, scale=0.1, alpha=0.5) #color', 'b', 'label')
# T1.plot(length=0.4, style='line', frame='1', flo=(0.07, 0, -0.01))
# cam2.plot_camera(ax=ax, scale=0.1, alpha=0.5) #'color', 'r', 'label')
# T2.plot(length=0.4, style='line', frame='2', flo=(0.09, 0, -0.02))

cam1.plot(ax=ax, scale=0.15, alpha=0.7, shape='camera', color='b') #color', 'b', 'label')
T1.plot(length=0.4, style='line', color='b', frame='1', flo=(0.07, 0, -0.01))
cam2.plot(ax=ax, scale=0.15, alpha=0.7, shape='camera', color='r') #'color', 'r', 'label')
T2.plot(length=0.4, style='line', color='r', frame='2', flo=(0.09, 0, -0.04))

P = [0.5, 0.1, 0.8]
plot_sphere(0.03, P, color='b', ax=ax)

ax.view_init(22, -118)

# rvcprint.rvcprint
rvcprint.rvcprint()