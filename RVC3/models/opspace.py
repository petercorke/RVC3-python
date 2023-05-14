#! /usr/bin/env python

"""
Creates Fig 9.25 using pure Python code
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import numpy as np
from scipy import linalg
import bdsim
from roboticstoolbox import models
import spatialmath.base as smb
from spatialmath import SE3

# equation numbers are with reference to:
#  A Unified Approach for Motion and Force Control of Robot Manipulators: The
#  Operational Space Formulation, Khatib, IEEE J.Robotics, RA-3/1, Feb 1987.
#   http://khatib.stanford.edu/publications/pdfs/Khatib_1987_RA.pdf


robot = models.DH.Puma560().nofriction()
T_E = SE3(0.6, -0.2, 0.8) * SE3.OA([0, 1, 0], [0, 0, -1])
sol = robot.ikine_a(T_E)

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
Fstar = np.r_[0, 0, -5, 0, 0, 0]
Xstar = np.r_[0.8, 0.2, 0.3, 0, np.pi / 2, 0]

# control parameters
Kvf = 20.0
Kf = 20.0
Kp = 100.0
Kv = 50.0

# choose a representation that is singularity free for tool down configuration
rep = "rpy/xyz"

## create block diagram
sim = bdsim.BDSim(graphics=True)
bd = sim.blockdiagram(name="opspace")

# blocks
robot_x = bd.FDYN_X(robot, q0=sol.q, gravcomp=True, velcomp=True, representation=rep)

fstar = bd.CONSTANT(Fstar, name="f*")
xstar = bd.CONSTANT(Xstar, name="x*")
xdstar = bd.CONSTANT(np.zeros((6,)), name="xd*")

fprod = bd.PROD("**", matrix=True, name="fprod")
pprod = bd.PROD("**", matrix=True, name="pprod")
fsum = bd.SUM("+-", name="fsum")


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


ftsensor = bd.FUNCTION(ft_sensor_func, name="f/t sensor")


# x error
def x_error_func(x1, x2):
    e = x1 - x2
    e[3:] = smb.angdiff(e[3:])
    return e


x_error = bd.FUNCTION(x_error_func, nin=2, name="xerror")

Mx = bd.INERTIA_X(robot, representation=rep)

# scopes
pos_scope = bd.SCOPE(
    vector=3, labels=["x", "y", "z"], styles=["r", "g", "b--"], name="position"
)
force_scope = bd.SCOPE(vector=6, name="force/torque")
wrench_scope = bd.SCOPE(
    vector=3, labels=["x", "y", "z"], styles=["r", "g", "b--"], name="command wrench"
)
xe_scope = bd.SCOPE(vector=6, name="x error")
fsum_scope = bd.SCOPE(vector=6, name="fsum scope")
fprod_scope = bd.SCOPE(vector=6, name="fprod scope")
sum1_scope = bd.SCOPE(vector=6, name="_sum1 scope")
x_scope = bd.SCOPE(vector=6, name="x scope")

##  connect the blocks

# force control
fsum[0] = omega_f * (fstar + (fstar - ftsensor) * Kf)
fsum[1] = fprod
fprod[1] = omega_f * Kvf * robot_x.xd

# position control
pprod[1] = omega_p * (Kp * x_error + Kv * (xdstar - robot_x.xd))
x_error[0] = xstar
x_error[1] = robot_x.x

# the rest
robot_x.w = fsum + pprod
Mx[0] = robot_x.q
bd.connect(Mx, fprod[0], pprod[0])
ftsensor[0] = robot_x.x
x_scope[0] = robot_x.x

pos_scope[0] = robot_x.x >> bd.INDEX([0, 1, 2])
force_scope[0] = ftsensor
wrench_scope[0] = pprod >> bd.INDEX([0, 1, 2])
xe_scope[0] = x_error
fsum_scope[0] = fsum
fprod_scope[0] = fprod
sum1_scope[0] = bd["_sum.1"]

bd.compile()  # check the diagram
sim.report(bd, sortby="type")

if __name__ == "__main__":
    out = sim.run(
        bd, 2, dt=5e-3, watch=[x_error, pprod, robot_x.x, robot_x.xd, robot_x.xdd]
    )
