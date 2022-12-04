#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

np.set_printoptions(linewidth=150)

# camera = CentralCamera.Default(pose=SE3(-0.3, 0.2, -2)*SE3.Rz(np.pi/2))
camera = CentralCamera.Default(pose=SE3(0, 0, -2)*SE3.Rz(np.pi))

P = mkgrid(2, 0.5, pose=SE3(0, 0, 2))

#Tc0 = transl(-0.3, 0.2, -2)*trotz[0]

lmbda=0.1
vs = IBVS_polar(camera, lmbda=lmbda, P=P, pose_d=SE3(0, 0, 1), depth=2, graphics=False)

vs.run(5000)

plt.figure()
vs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)

plt.figure()
vs.plot_pose()
rvcprint.rvcprint(subfig='b')

