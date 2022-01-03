#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3


camera = CentralCamera(f=0.015, rho=10e-6,
    imagesize=[1280, 1024], pp=[640, 512], name='mycamera')


X, Y, Z = mkcube(0.2, pose=SE3(0, 0, 1), edge=True)

camera.plot_wireframe(X, Y, Z, color='k')
rvcprint.rvcprint(subfig='a', facecolor=None)

#----------------------------------------------------------------------- #

# T_camera = SE3(-1, 0, 0.5) * SE3.Ry(0.8)
T_camera = SE3(-1, 0, 0.5) * SE3.Ry(0.9)
camera.clf()
camera.plot_wireframe(X, Y, Z, pose=T_camera, color='k')
rvcprint.rvcprint(subfig='b', facecolor=None)
