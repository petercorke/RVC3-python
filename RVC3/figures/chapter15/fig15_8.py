#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default(pose=SE3(1, 0.5, -3) * SE3.Rz(0.6))

P = mkgrid(2, 0.5, pose=SE3(-1, -1, 2))
pd = 200 * np.array([[-1, -1, 1, 1], [-1, 1, 1, -1]]) + np.c_[camera.pp]

ibvs = IBVS(camera, P=P, pd=pd, depth=3)
ibvs.run(25)

plt.figure()
ibvs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

plt.clf()
ibvs.plot_vel()
rvcprint.rvcprint(subfig='b')
# ------------------------------------------------------------------------- #

plt.clf()
ibvs.plot_pose()
rvcprint.rvcprint(subfig='c')
# ------------------------------------------------------------------------- #

plt.clf()
ibvs.plot_jcond()
rvcprint.rvcprint(subfig='d')

