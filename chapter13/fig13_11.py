#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from spatialmath.base import plot_sphere

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
est.plot_camera(scale=0.3)
plot_sphere(0.03, P, color='r')
SE3().plot(frame='T', color='b', length=0.3)
ax = plt.gca()
ax.set_xlim3d(-0.9, 0.9)
ax.set_ylim3d(-0.9, 0.9)
ax.set_zlim3d(-1.5, 0.3)

rvcprint.rvcprint()