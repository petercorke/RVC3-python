#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3


camera = CentralCamera(f=0.015, rho=10e-6,
    imagesize=[1280, 1024], pp=[640, 512], name='mycamera')


P = mkgrid(3, 0.2, pose=SE3(0, 0, 1.0))

camera.plot_point(P)
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

T_camera = SE3(-1, 0, 0.5) * SE3.Ry(0.9)

camera.clf()
camera.plot_point(P, pose=T_camera)

rvcprint.rvcprint(subfig='b')

