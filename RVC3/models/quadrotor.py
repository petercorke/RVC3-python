#! /usr/bin/env python

"""
Creates Fig 4.24
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from enum import IntEnum
import numpy as np
from spatialmath import SO2
from bdsim.blockdiagram import BlockDiagram
from math import pi, sqrt, atan, atan2
import bdsim


# dict of quadrotor parameters
from RVC3.models.quad_model import quadrotor

sim = bdsim.BDSim(animation=True)
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


# demand signals
x_dmd = bd.WAVEFORM("sine", freq=0.25, unit="Hz", phase=0.25)
y_dmd = bd.WAVEFORM("sine", freq=0.25, unit="Hz")
xy_dmd = bd.MUX(nin=2, inputs=(x_dmd, y_dmd), name="xy_demand")

yaw_dmd = bd.RAMP(slope=0.1, T=3, off=0, name="yaw demand")

z_dmd = bd.INTERPOLATE(
    (0, 0.5, 5.5, np.inf), (0, 0, -5, -5), time=True, name="height demand"
)


# yaw control
def yaw_controller(yaw_dmd, x):
    r = x["rot"]
    return (Kp_yaw) * (yaw_dmd - r[E.YW] - Kd_yaw * r[E.YWD])


yaw = bd.FUNCTION(yaw_controller, nin=2, nout=1, name="yawcontrol")


# height control
def height_controller(height_dmd, x):
    t = x["trans"]
    T = (-Kp_z) * (height_dmd - t[E.Z] - Kd_z * t[E.ZD]) + T0
    # print('h', x[2], z, x[8])
    return -T


height = bd.FUNCTION(height_controller, nin=2, nout=1, name="zcontrol")


# velocity control
def velocity_controller(xy_dmd, x):
    t = x["trans"]
    xyerr_0 = xy_dmd - t[[E.X, E.Y]]
    xyerr_B = SO2(-x["rot"][E.YW]) * xyerr_0  # in {B}
    K = Kp_xy * np.array([[0, 1], [-1, 0]])
    return K @ (xyerr_B.ravel() - Kd_xy * t[[E.XD, E.YD]])


velocity = bd.FUNCTION(velocity_controller, nin=2, nout=1, name="velcontrol")


# attitude control
def attitude_controller(rp_dmd, x):
    r = x["rot"]
    rp_torque = (Kp_rp) * (rp_dmd - r[[E.R, E.P]] - Kd_rp * r[[E.RD, E.PD]])
    return list(rp_torque)


attitude = bd.FUNCTION(attitude_controller, nin=2, nout=2, name="attitudecontrol")

# drone + input mixer
mixer = bd.MULTIROTORMIXER(quadrotor, name="mixer", wmax=1500)
quad = bd.MULTIROTOR(quadrotor, name="quadrotor")

# plot abs value of rotor speeds
abs_rotorspeed = bd.FUNCTION(lambda x: np.abs(x), name="absval")
scope_rotorspeed = bd.SCOPE(
    vector=4, labels=list("0123"), name="rotor speed (abs.val)", inputs=abs_rotorspeed
)

# plot position and attitude
x = bd.ITEM("x", name="state")
xyz = bd.SLICE1([0, 1, 2], inputs=x)
scope_xyz = bd.SCOPE(vector=3, labels=list("XYZ"), name="position", inputs=xyz)
att = bd.SLICE1([3, 4, 5], inputs=x)
scope_attitude = bd.SCOPE(
    vector=3, labels=["yaw", "pitch", "roll"], name="attitude", inputs=att
)

# animation of quad
quadplot = bd.MULTIROTORPLOT(quadrotor)

# wiring
bd.connect(quad, yaw[1], height[1], velocity[1], attitude[1], x)  # state
bd.connect(yaw_dmd, yaw[0])
bd.connect(z_dmd, height[0])
bd.connect(xy_dmd, velocity[0])
bd.connect(velocity, attitude[0])
bd.connect(attitude, mixer[:2])
bd.connect(yaw, mixer[2])
bd.connect(height, mixer[3])
bd.connect(mixer, quad, abs_rotorspeed)
bd.connect(quad, quadplot)

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
