#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default(name='')

P = mkgrid(2, 0.5, pose=SE3(0, 0, 2))
pd = 200 * np.array([[-1, -1, 1, 1], [-1, 1, 1, -1]]) + np.c_[camera.pp]
ibvs = IBVS(camera, P=P, p_f=pd, depth=3)

## 2 rad
ibvs.pose_0=SE3(0, 0, -1) * SE3.Rz(2)
ibvs.run(50)

plt.figure()
ibvs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

plt.clf()
ibvs.plot_pose()
rvcprint.rvcprint(subfig='b')
# ------------------------------------------------------------------------- #


# Chaumette conundrum
ibvs.pose_0 = SE3(0, 0, -1) * SE3.Rz(np.piq)
ibvs.run(10)

plt.figure()
ibvs.plot_p()
rvcprint.rvcprint(subfig='c', facecolor=None)
# ------------------------------------------------------------------------- #

plt.clf()
ibvs.plot_pose()
rvcprint.rvcprint(subfig='d')
# ------------------------------------------------------------------------- #

