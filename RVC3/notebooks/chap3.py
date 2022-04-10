# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from math import pi
np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)

from spatialmath import *
from spatialmath.base import *
from roboticstoolbox import *

# ------------------------------ #


# Time-Varying Pose


# Rate of Change of Orientation


# Rate of Change of Pose


# Transforming Spatial Velocities

aTb = SE3.Tx(-2) * SE3.Rz(-pi/2) * SE3.Rx(pi/2);
bV = [1, 2, 3, 4, 5, 6];
aJb = aTb.jacob();
aJb.shape
aV = aJb @ bV
aV = aTb.Ad() @ [1, 2, 3, 0, 0, 0]
aV = aTb.Ad() @ [0, 0, 0, 1, 0, 0]
aV = aTb.Ad() @ [1, 2, 3, 1, 0, 0]

# Incremental Rotation

rotx(0.001)
import time
Rexact = np.eye(3); Rapprox = np.eye(3);  # null rotation
w = np.array([1, 0, 0]);   # rotation of 1rad/s about x-axis
dt = 0.01;            # time step
t0 = time.process_time();
for i in range(100):  # exact integration over 100 time steps
  Rexact = Rexact @ trexp(skew(w*dt));       # update by composition
print(time.process_time() - t0)
t0 = time.process_time();
for i in range(100):  # approximate integration over 100 time steps
  Rapprox = Rapprox + Rapprox @ skew(w*dt);  # update by addition
print(time.process_time() - t0)
np.linalg.det(Rapprox) - 1
np.linalg.det(Rexact) - 1
tr2angvec(trnorm(Rexact))
tr2angvec(trnorm(Rapprox))

# Incremental Rigid-Body Motion


# Accelerating Bodies and Reference Frames


# Dynamics of Moving Bodies

J = np.array([[ 2, -1, 0],
              [-1,  4, 0],
              [ 0,  0, 3]]);
orientation = UnitQuaternion();  # identity quaternion
w = 0.2 * np.array([1, 2, 2]);
dt = 0.05;  # time step
def update():
  global orientation, w
  for t in np.arange(0, 10, dt):
     wd = -np.linalg.inv(J) @ (np.cross(w, J @ w))  # (3.12)
     w += wd * dt
     orientation *= UnitQuaternion.EulerVec(w * dt)
     yield orientation.R
tranimate(update())

# Transforming Forces and Torques

bW = [1, 2, 3, 0, 0, 0];
aW = aTb.inv().Ad().T @ bW

# Inertial Reference Frame


# Creating Time-Varying Pose


# Smooth One-Dimensional Trajectories

traj = quintic(0, 1, np.linspace(0, 1, 50));
traj.plot();
quintic(0, 1, np.linspace(0, 1, 50), qd0=10, qdf=0);
qd = traj.qd;
qd.mean() / qd.max()
traj = trapezoidal(0, 1, np.linspace(0, 1, 50));
traj.plot();
traj.qd.max()
traj1_2 = trapezoidal(0, 1, np.linspace(0, 1, 50), V=1.2);
traj2_0 = trapezoidal(0, 1, np.linspace(0, 1, 50), V=2);

# Multi-Axis Trajectories

traj = mtraj(trapezoidal, [0, 2], [1, -1], 50);
traj.plot();

# Multi-Segment Trajectories

via = SO2(30, unit="deg") * np.array([[-1, 1, 1, -1, -1], [1, 1, -1, -1, 1]]);
traj0 = mstraj(via.T, dt=0.2, tacc=0, qdmax=[2, 1]);
xplot(traj0.q[:, 0], traj0.q[:, 1], color="red");
traj2 = mstraj(via.T, dt=0.2, tacc=2, qdmax=[2, 1]);
len(traj0), len(traj2)

# Interpolation of Orientation in 3D

R0 = SO3.Rz(-1) * SO3.Ry(-1);
R1 = SO3.Rz(1) * SO3.Ry(1);
rpy0 = R0.rpy(); rpy1 = R1.rpy();
traj = mtraj(quintic, rpy0, rpy1, 50);
pose = SO3.RPY(traj.q);
len(pose)
pose.animate();
q0 = UnitQuaternion(R0); q1 = UnitQuaternion(R1);
qtraj = q0.interp(q1, 50);
len(qtraj)
qtraj.animate()

# Direction of Rotation

q0 = UnitQuaternion.Rz(-2); q1 = UnitQuaternion.Rz(2);
q = q0.interp(q1, 50);
q.animate()
q = q0.interp(q1, 50, shortest=True);
q.animate()

# Cartesian Motion in 3D

T0 = SE3.Trans([0.4, 0.2, 0]) * SE3.RPY(0, 0, 3);
T1 = SE3.Trans([-0.4, -0.2, 0.3]) * SE3.RPY(-pi/4, pi/4, -pi/2);
T0.interp(T1, 0.5)
Ts = T0.interp(T1, 51);
len(Ts)
Ts.animate()
Ts[25]
P = Ts.t;
P.shape
xplot(P, labels="x y z");
rpy = Ts.rpy();
xplot(rpy, labels="roll pitch yaw");
Ts = T0.interp(T1, trapezoidal(0, 1, 50).q);
Ts = ctraj(T0, T1, 50);

# Application: Inertial Navigation


# Gyroscopes


# How Gyroscopes Work


# Estimating Orientation

from imu_data import IMU
true, _ = IMU()
orientation = UnitQuaternion();  # identity quaternion
for w in true.omega[:-1]:
  next = orientation[-1] @ UnitQuaternion.EulerVec(w * true.dt);
  orientation.append(next);
len(orientation)
orientation.animate(time=true.t)
xplot(true.t, orientation.rpy(), labels="roll pitch yaw");

# Accelerometers


# How Accelerometers Work


# Estimating Pose and Body Acceleration


# Magnetometers


# How Magnetometers Work


# Estimating Heading


# Inertial Sensor Fusion

from imu_data import IMU
true, imu = IMU()
q = UnitQuaternion();
for wm in imu.gyro[:-1]:
  q.append(q[-1] @ UnitQuaternion.EulerVec(wm * imu.dt))
xplot(true.t, q.angdist(true.orientation), color="red");
kI = 0.2; kP = 1;
b = np.zeros(imu.gyro.shape);
qcf = UnitQuaternion();
data = zip(imu.gyro[:-1], imu.accel[:-1], imu.magno[:-1]);
for k, (wm, am, mm) in enumerate(data):
  qi = qcf[-1].inv()
  sR = np.cross(am, qi * true.g) + np.cross(mm, qi * true.B)
  wp = wm - b[k,:] + kP * sR
  qcf.append(qcf[k] @ UnitQuaternion.EulerVec(wp * imu.dt))
  b[k+1,:] = b[k,:] - kI * sR * imu.dt
xplot(true.t, qcf.angdist(true.orientation), color="blue");

# Wrapping Up


# Further Reading


# Exercises

