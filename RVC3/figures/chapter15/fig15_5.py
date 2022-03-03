#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

from spatialmath import SE3

camera = CentralCamera.Default(pose=SE3(1, 0.5, -3) * SE3.Rz(0.6))
P = mkgrid(2, 0.5)
cdTg = SE3(0, 0, 1)
pbvs = PBVS(camera, pose_g=SE3(-1, -1, 2), pose_d=cdTg, P=P, 
    plotvol=[-1, 2, -1, 2, -3, 2.5], eterm=.001, graphics=False)

pbvs.run(200)

plt.figure()
pbvs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

plt.clf()
pbvs.plot_vel()
# l = findobj('type', 'legend')
# l.FontSize = 10
rvcprint.rvcprint(subfig='b')
# ------------------------------------------------------------------------- #

plt.clf()
pbvs.plot_pose()
# l = findobj('type', 'legend')
# l[0].FontSize = 10
# l[1].FontSize = 10

rvcprint.rvcprint(subfig='c')

