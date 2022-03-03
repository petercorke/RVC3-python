#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from spatialmath.base import plot_sphere, plotvol3

P = mkcube(0.2)

T_unknown = SE3(0.1, 0.2, 1.5) * SE3.RPY(0.1, 0.2, 0.3)

camera = CentralCamera(f=0.015, rho=10e-6, imagesize=[1280, 1024], \
    noise=0.05)

p = camera.project_point(P, objpose=T_unknown)

C, resid = CentralCamera.points2C(P, p)

est = CentralCamera.decomposeC(C)

est.f / est.rho[0]

camera.f / camera.rho[1]

(T_unknown * est.pose).printline()

# plt.clf()
plotvol3([-0.9, 0.9, -0.9, 0.9, -1.5, 0.3])
est.plot(scale=0.3, shape='camera', color='k', frame=True)
# est.pose.plot(length=0.4, style='line', color='b', flo=(0.07, 0, -0.01))

plot_sphere(0.03, P, color='k')
SE3().plot(frame='T', color='b', length=0.3)


rvcprint.rvcprint(interval=(0.4, 0.4, 0.2))