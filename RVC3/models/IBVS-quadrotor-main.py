#! /usr/bin/env python

"""
Creates Fig 16.9
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path
from enum import IntEnum
from machinevisiontoolbox import *
from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt
from math import pi

# dict of quadrotor parameters
from RVC3.models.quad_model import quadrotor

sim = BDSim(animation=True)  # debug='i')
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


# ---------------------------------- camera and vision

camera = SphericalCamera()
# create a grid of points on the ground
P = mkgrid(2, 4)

# set the desired view of these points, defines the final pose of the quad
pd = camera.project_point(P, pose=SE3(0, 0, -5) * SE3.Rz(0))  # pi/2))


def plot_init(camera):
    camera.plot_point(pd, "b*")


# ---------------------------------- quadrotor and control

# dict of quadrotor parameters
from RVC3.models.quad_model import quadrotor

# controller parameters
Kp_yaw = 20
Kd_yaw = 1
Kp_z = 4
Kd_z = 1
T0 = 40
Kp_xy = 0.1
Kd_xy = 1
Kp_rp = 100
Kd_rp = 1


# yaw rate control
def yaw_rate_controller(yawdot_dmd, X):
    rot = X["rot"]
    yawdot = rot[E.YWD]
    # cmd = (-Kp_yaw) * (yawdot_dmd - Kd_yaw * yawdot)
    cmd = (Kd_yaw) * (yawdot_dmd - yawdot)
    # print(f"YAW: {yaw=} {yawdot_dmd=} {yawdot=} {cmd=}")
    return cmd


# # yaw control
# def yaw_controller(yaw_dmd, x):
#     r = x["rot"]
#     return [(Kp_yaw) * (yaw_dmd - r[E.YW] - Kd_yaw * r[E.YWD]), r[E.YW]]


# height rate control
# def altitude_rate_controller(zdot_dmd, X):
#     zdot = X["trans"][E.ZD]
#     Tz = T0 + (-Kp_z) * (zdot_dmd - Kd_z * zdot)
#     z = X["x"][2]
#     # print('h', x[2], z, x[8])
#     # print(f"HEIGHT: {z=} {zdot_dmd=} {zdot=} {Tz=}")
#     return Tz


def altitude_rate_controller(zdot_dmd, X):
    zdot = X["trans"][E.ZD]
    Tz = T0 + (-Kd_z) * (zdot_dmd - zdot)
    # z = X["x"][2]
    # print('h', x[2], z, x[8])
    # print(f"HEIGHT: {z=} {zdot_dmd=} {zdot=} {Tz=}")
    return Tz


# z-axis is downwards so:
#  x velocity requires -ve pitch
#  y velocity requires +ve roll
FLIP = np.array([[0, 1], [-1, 0]])


# # velocity control
# def velocity_controller(xydot_dmd, X):
#     xydot = X["vb"][:2]
#     cmd = FLIP @ (Kp_xy * (xydot_dmd - Kd_xy * xydot))
#     xy = X["x"][:2]
#     # print(f"VELXY: {xy=} {xydot_dmd=} {xydot=} {cmd=}")
#     return cmd


# # attitude control
# def attitude_controller(rp_dmd, X):
#     rp = X["x"][3:5]
#     rpdot = X["w"][:2]
#     rp_torque = (-Kp_rp) * (rp_dmd - rp - Kd_rp * rpdot)
#     # print(f"ATTITUDE: {rp=} {rp_dmd=} {rpdot=} {rp_torque=}")
#     return list(rp_torque)


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
model = Path(__file__).parent / "IBVS-quadrotor.bd"
print(model)

bd = bdload(bd, model, globalvars=globals(), verbose=False)
bd.compile()

sim.report(bd)
out = sim.run(bd, 1)
print(out)
