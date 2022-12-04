#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

camera = SphericalCamera(pose=SE3(0.3, 0.3, -2)*SE3.Rz(1))

P = mkgrid(2, side=1.5, pose=SE3(0, 0, 0.5))
pose_f = SE3(0, 0, -1.5)

vs = IBVS_sph(camera, P=P, pose_d=pose_f, verbose=False, graphics=False)
vs.run(200)

vs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None, debug=False)
# ------------------------------------------------------------------------- #


camera = SphericalCamera(pose=SE3(0.3, 0.3, -2)*SE3.Rz(0.4))
vs = IBVS_sph(camera, P=P, pose_d=pose_f, verbose=False, lmbda=0, graphics=True)
vs.run(1)
vs.ax_camera.remove()
vs.ax_3dview.view_init(22, 54)
vs.ax_3dview.set_box_aspect((1, 1, 1.3))
rvcprint.rvcprint(subfig='b', thicken=None)
