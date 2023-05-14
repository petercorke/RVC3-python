#! /usr/bin/env python

"""
Creates Fig 9.25 using opspace.bd model
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import numpy as np
from scipy import linalg
from pathlib import Path
from bdsim import BDSim, bdload
from roboticstoolbox import models
from spatialmath import SE3
import spatialmath.base as smb

robot = models.DH.Puma560().nofriction()

T_E = SE3(0.6, -0.2, 0.8) * SE3.OA([0, 1, 0], [0, 0, -1])
sol = robot.ikine_a(T_E)
q0 = sol.q

# compliance frame is EE frame, constant in this case
Sf = T_E.R

# compliance specification
# edit next 2 lines to change compliant motion axes
#  1 = freespace controlled motion
#  0 = constrained compliant motion
sigma_t = np.diag([1, 1, 0])
# position specification matrix, Sigma_f in (1)
sigma_r = np.diag([1, 1, 1])
# rotation specification matrix, Sigma_tau

# compute the generalized task specification matrices (3) and (4)
omega_p = linalg.block_diag(Sf.T @ sigma_t @ Sf, Sf.T @ sigma_r @ Sf)
one = np.eye(3)
omega_f = linalg.block_diag(Sf.T @ (one - sigma_t) @ Sf, Sf.T @ (one - sigma_r) @ Sf)

# setpoints
Fstar = np.r_[0.0, 0, -5, 0, 0, 0]
Xstar = np.r_[0.8, 0.2, 0.3, 0, np.pi / 2, 0]
Xdstar = np.r_[0.0, 0, 0, 0, 0, 0]

# control parameters
Kvf = 20.0
Kf = 20.0
Kp = 100.0
Kv = 50.0


# force/torque sensor
def ft_sensor_func(x):
    z = x[2]
    surface = 0.5
    stiffness = 100

    if z <= surface:
        f = stiffness * (z - surface)
    else:
        f = 0
    return np.r_[0, 0, f, 0, 0, 0]


# x error
def x_error_func(x1, x2):
    e = x1 - x2
    e[3:] = smb.angdiff(e[3:])
    return e


sim = BDSim(graphics=True)

bd = sim.blockdiagram()
model = Path(__file__).parent / "opspace.bd"
bd = bdload(bd, model, globalvars=globals(), verbose=True)
bd.compile()
sim.report(bd)
out = sim.run(
    bd,
    2,
    dt=5e-3,
)
print(out)
