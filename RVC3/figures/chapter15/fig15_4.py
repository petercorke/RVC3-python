#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default(pose = SE3(1, 0.5, -3) * SE3.Rz(0.6))
P = mkgrid(2, 0.5)
T_Cd_B = SE3(0, 0, 1)
pbvs = PBVS(camera, pose_g=SE3(-1, -1, 2), pose_d=T_Cd_B, P=P, plotvol=[-1, 2, -1, 2, -3, 2.5])

pbvs.run(100)


rvcprint.rvcprint(debug=False, facecolor=None)


