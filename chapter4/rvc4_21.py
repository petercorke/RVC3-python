#!/usr/bin/env python3

from enum import IntEnum
import numpy as np
from spatialmath import SO2
from bdsim.blockdiagram import BlockDiagram
from math import pi, sqrt, atan, atan2
import bdsim


sim = bdsim.BDSim(progress=True)
bd = sim.blockdiagram()

# state vector indices
#   would expect the order to R, P, Y but this is compatible with the
#   MATLAB version
class State(IntEnum):
    X = 0
    Y = 1
    Z = 2
    YW = 3
    P = 4
    R = 5
    XD = 6
    YD = 7
    ZD = 8
    YWD = 9
    PD = 10
    RD = 11

# controller parameters
Kp_yaw = 20
Kd_yaw = 2
Kp_z = 4
Kd_z = 1
T0 = 40
Kp_xy = 0.1
Kd_xy = 2
Kp_rp = 100
Kd_rp = 1

# dict of quadrotor parameters
from bdsim.blocks.quad_model import quadrotor

# demand signals
x_dmd = bd.WAVEFORM('sine', freq=0.25, unit='Hz', phase=0.25)
y_dmd = bd.WAVEFORM('sine', freq=0.25, unit='Hz')
xy_dmd = bd.MUX(nin=2, inputs=(x_dmd, y_dmd))
yaw_dmd = bd.RAMP(slope=0.4, T=1, off=0)
z_dmd = bd.CONSTANT(-4)

# yaw control
def yaw_controller(x, yaw_dmd):
    return (-Kp_yaw) * (yaw_dmd - x[State.YW] - Kd_yaw * x[State.YWD])

yaw = bd.FUNCTION(yaw_controller, nin=2, nout=1, name='yawcontrol')

# height control
def height_controller(x, height_dmd):
    return (-Kp_z) * (height_dmd - x[State.Z] - Kd_z * x[State.ZD]) + T0

height = bd.FUNCTION(height_controller, nin=2, nout=1, name='zcontrol')

# velocity control
def velocity_controller(x, xy_dmd):
    xyerr_0 = xy_dmd - x[[State.R, State.P]]
    xyerr_B = SO2(-x[State.YW]) * xyerr_0  # in {B}
    K = Kp_xy * np.array([[0, 1], [-1, 0]])
    return K @ (xyerr_B.ravel() - Kd_xy * x[State.XD:State.ZD])

velocity = bd.FUNCTION(velocity_controller, nin=2, nout=1, name='velcontrol')

# attitude control
def attitude_controller(x, rp_dmd):
    rp_torque = (-Kp_rp) * (rp_dmd - x[[State.R, State.P]] - Kd_rp * x[[State.RD, State.PD]])
    return list(rp_torque)

attitude = bd.FUNCTION(attitude_controller, nin=2, nout=2, name='attitudecontrol')

# mixer
def mixer_controller(tau_r, tau_p, tau_y, thrust):
    signs = np.r_[1, -1, 1, -1]
    w = np.r_[tau_p, -tau_r, -tau_p, tau_r] + tau_y * signs + thrust / quadrotor['nrotors']
    w = np.clip(w, 5, 1000) * signs
    w = np.sign(w) * np.sqrt(np.abs(w) / quadrotor['b'])
    return w

mixer = bd.FUNCTION(mixer_controller, nin=4, nout=1, name='mixer')

quad = bd.MULTIROTOR(quadrotor, name='quadrotor')

# wiring

bd.connect(quad, yaw[0], height[0], velocity[0], attitude[0])
bd.connect(yaw_dmd, yaw[1])
bd.connect(z_dmd, height[1])
bd.connect(xy_dmd, velocity[1])

bd.connect(velocity, attitude[1])

bd.connect(attitude[0], mixer[0])
bd.connect(attitude[1], mixer[1])
bd.connect(yaw, mixer[2])
bd.connect(height, mixer[3])
bd.connect(mixer, quad)

quadplot = bd.MULTIROTORPLOT(quadrotor)
bd.connect(quad, quadplot)

# debug
# bd.PRINT(yaw_dmd, fmt='{:.3f}', name='yawdmd')
# bd.PRINT(yaw, fmt='{:.3f}', name='yaw')


# build it
bd.compile()

if __name__ == "__main__":
    bd.report()
    out = sim.run(bd, T=5, dt=0.05)

    bd.done(block=True)


# np.set_printoptions(linewidth=300, suppress=True, precision=4)
# quad.setstate(np.r_[1, 2, -3, 0.1, 0.2, 0.3,  0.1, 0.2, 0.3, 0.1, 0,2, 0.3])

# quad.inputs = [900 * np.r_[1, .9, 1.1, 1]]

# # check outputs
# x = quad.output(t=0)
# xd = quad.deriv()

# print('x: ', x)
# print('xd:', xd)