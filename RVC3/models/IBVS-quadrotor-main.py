from pathlib import Path
from machinevisiontoolbox import *
from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt
from math import pi


sim = BDSim(animation=True) #debug='i')
bd = sim.blockdiagram()


# ---------------------------------- camera and vision
lmbda = 0.1

camera = SphericalCamera()
# create a grid of points on the ground
P = mkgrid(2, 4)

# set the desired view of these points, defines the final pose of the quad
pd = camera.project_point(P, pose=SE3(0, 0, -5)*SE3.Rz(0)) #pi/2))


def plot_init(camera):
	camera.plot_point(pd, 'b*')

# ---------------------------------- quadrotor and control

# dict of quadrotor parameters
from bdsim.blocks.quad_model import quadrotor

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
	yaw = X['x'][5]
	yawdot = X['w'][2]
	cmd = (-Kp_yaw) * (yawdot_dmd - Kd_yaw * yawdot)
	# print(f"YAW: {yaw=} {yawdot_dmd=} {yawdot=} {cmd=}")
	return cmd

# height rate control
T0 = 40

def altitude_rate_controller(zdot_dmd, X):
	zdot = X['vb'][2]
	Tz =  T0 + (-Kp_z) * (zdot_dmd - Kd_z * zdot)
	z = X['x'][2]
    # print('h', x[2], z, x[8])
	# print(f"HEIGHT: {z=} {zdot_dmd=} {zdot=} {Tz=}")
	return Tz

# z-axis is downwards so:
#  x velocity requires -ve pitch
#  y velocity requires +ve roll
FLIP = np.array([[0, 1], [-1,0]])

# velocity control
def velocity_controller(xydot_dmd, X):
	xydot = X['vb'][:2]
	cmd =  FLIP @ (Kp_xy * (xydot_dmd - Kd_xy * xydot))
	xy = X['x'][:2]
	# print(f"VELXY: {xy=} {xydot_dmd=} {xydot=} {cmd=}")
	return cmd

# attitude control
def attitude_controller(rp_dmd, X):
	rp = X['x'][3:5]
	rpdot = X['w'][:2]
	rp_torque = (-Kp_rp) * (rp_dmd - rp - Kd_rp * rpdot)
	# print(f"ATTITUDE: {rp=} {rp_dmd=} {rpdot=} {rp_torque=}")
	return list(rp_torque)

# ----------------------------------
model = Path(__file__).parent / "IBVS-quadrotor.bd"
print(model)

bd = bdload(bd, model, globalvars=globals(), verbose=True)
bd.compile()
bd.report()

print(sim.options)
sim.set_options(animation=False)
out = sim.run(bd, 1)
print('done')
print(out)

# sim.done(bd)
# plt.pause(5)
