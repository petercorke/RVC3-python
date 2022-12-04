#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3

camera = CentralCamera.Default(pose=SE3(1, 0.5, -3) * SE3.Rz(0.6))

P = mkgrid(2, 0.5, pose=SE3(-1, -1, 2))
pd = 200 * np.array([[-1, -1, 1, 1], [-1, 1, 1, -1]]) + np.c_[camera.pp]

ibvs = IBVS(camera, P=P, p_d=pd, depthest=True)
ibvs.run(50)

plt.figure()
ibvs.plot_p()
rvcprint.rvcprint(subfig='a', facecolor=None)
# ------------------------------------------------------------------------- #

plt.clf()
Ze = [h.Z_est for h in ibvs.history]
Zt = [h.Z_true for h in ibvs.history]
plt.plot(np.array(Zt))
plt.plot(np.array(Ze), '--')
labels_t = [f"$Z_{i}$" for i in range(4)]
labels_e = [f"$\hat{{Z}}_{i}$" for i in range(4)]
plt.legend(labels_t + labels_e, loc='upper right')
plt.grid(True)
plt.xlabel('Time step')
plt.xlim(0, len(ibvs.history))
plt.ylabel('Depth (m)')
plt.ylim(0.5, 4)
rvcprint.rvcprint(subfig='b')
# ------------------------------------------------------------------------- #
