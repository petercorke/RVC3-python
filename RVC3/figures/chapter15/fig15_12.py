#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default()
P = mkgrid(2, side=0.5)

# camera with respect to goal
T_Cd_B = SE3(0, 0, 0.7)
pbvs = PBVS(camera, pose_g=SE3(0, 0, 2), P=P, pose_d=T_Cd_B, plotvol=[-1, 2, -1, 2, -3, 0.5], graphics=False)
pbvs.pose_0 = pose=SE3(-0.2, 3.5, -3) * SE3.Rz(5 * np.pi/4)
pbvs.run(100)

plt.clf()
pbvs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

P = mkgrid(2, 0.5, pose=SE3(0, 0, 2))
pd = 200 * np.array([[-1, -1, 1, 1], [-1, 1, 1, -1]]) + np.c_[camera.pp]

ibvs = IBVS(camera, P=P, p_d=pd, lmbda=0.01, niter=-1, eterm=2, graphics=False)
ibvs.pose_0 = pbvs.pose_0
ibvs.run(500)
plt.clf()
ibvs.plot_p()

rvcprint.rvcprint(subfig='b', facecolor=None)
