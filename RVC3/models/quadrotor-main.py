#! /usr/bin/env python

"""
Creates Fig 4.24
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path

from enum import IntEnum
import numpy as np
from spatialmath import SE3, SO2
from bdsim import Clock, bdload, BDSim
from math import pi, sqrt, atan, atan2

# dict of quadrotor parameters
from RVC3.models.quad_model import quadrotor

sim = BDSim(animation=True)
bd = sim.blockdiagram()


# state vector indices
#   would expect the order to R, P, Y but this is compatible with the
#   MATLAB version
class E(IntEnum):
    X = 0
    Y = 1
    Z = 2
    XD = 3
    YD = 4
    ZD = 5

    YW = 0
    P = 1
    R = 2
    YWD = 3
    PD = 4
    RD = 5


# controller parameters
Kp_yaw = 100
Kd_yaw = 0.1
Kp_z = 40
Kd_z = 1
T0 = 40
Kp_xy = 0.1
Kd_xy = 2

Kp_rp = 20
Kd_rp = 0.1


# yaw control
def yaw_controller(yaw_dmd, x):
    r = x["rot"]
    return [(Kp_yaw) * (yaw_dmd - r[E.YW] - Kd_yaw * r[E.YWD]), r[E.YW]]


# height control
def height_controller(height_dmd, x):
    t = x["trans"]
    T = (-Kp_z) * (height_dmd - t[E.Z] - Kd_z * t[E.ZD]) + T0
    # print('h', x[2], z, x[8])
    return -T


# velocity control
def velocity_controller(xy_dmd, x):
    t = x["trans"]
    xyerr_B = xy_dmd.ravel() - t[[E.X, E.Y]]
    # xyerr_B = SO2(-x['rot'][E.YW]) * xyerr_0  # in {B}
    K = Kp_xy * np.array([[0, 1], [-1, 0]])
    return K @ (xyerr_B.ravel() - Kd_xy * t[[E.XD, E.YD]])


# attitude control
def attitude_controller(rp_dmd, x):
    r = x["rot"]
    rp_torque = (Kp_rp) * (rp_dmd - r[[E.R, E.P]] - Kd_rp * r[[E.RD, E.PD]])
    return list(rp_torque)


# ----------------------------------
model = Path(__file__).parent / "quadrotor.bd"

bd = bdload(bd, model, globalvars=globals(), verbose=False)

# build it
bd.compile()


if __name__ == "__main__":
    sim.report(bd)
    out = sim.run(bd, T=10, dt=0.05)

# np.set_printoptions(linewidth=300, suppress=True, precision=4)
# quad.setstate(np.r_[1, 2, -3, 0.1, 0.2, 0.3,  0.1, 0.2, 0.3, 0.1, 0,2, 0.3])

# quad.inputs = [900 * np.r_[1, .9, 1.1, 1]]

# # check outputs
# x = quad.output(t=0)
# xd = quad.deriv()

# print('x: ', x)
# print('xd:', xd)
