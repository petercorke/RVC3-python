#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

camera = SphericalCamera(pose=SE3(0.3, 0.3, -2)*SE3.Rz(0.4))

P = mkgrid(2, side=1.5, pose=SE3(0, 0, 0.5))
pose_f = SE3(0, 0, -1.5) * SE3.Rz(1)

vs = IBVS_sph(camera, P=P, pose_f=pose_f, verbose=True, graphics=False)
vs.run(50)

vs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #


camera = SphericalCamera(pose=SE3(0.3, 0.3, -2)*SE3.Rz(0.4))
vs = IBVS_sph(camera, P=P, pose_f=pose_f, verbose=True, graphics=True)
vs.run(1)
vs.ax_camera.remove()
rvcprint.rvcprint(subfig='b')
