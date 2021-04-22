# #  Chapter 3

# +
import time
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from math import pi, sqrt
import scipy as sp
# from sympy import simplify

from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE3, SO2, SO3, UnitQuaternion
from roboticstoolbox import tpoly, lspb, mtraj, qplot, ctraj, mstraj

np.set_printoptions(linewidth=120, formatter={'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})

# %config ZMQInteractiveShell.ast_node_interactivity = 'last_expr_or_assign'
# %matplotlib notebook
# -

# # Sec 3.1 Time-varying pose
# ## Sec. 3.1.2 transforming spatial velocity

aTb = SE3(-2, 0, 0) * SE3.Rz(-pi/2) * SE3.Rx(pi/2)

# +
wT = SE3()
aTb = SE3(-2, 0, 0) * SE3.Rz(-pi/2) * SE3.Rx(pi/2);

plotvol3(5)
wT.plot(frame='A', color='b')
aTb.plot(frame='B', color='r')
# -

# body to world frame
bV = [1, 2, 3, 4, 5, 6]

aV = aTb.jacob() @ bV

# same body
aV = aTb.Ad() @ [1, 2, 3, 0, 0, 0]

aV = aTb.Ad() @ [0, 0, 0, 1, 0, 0]

aV = aTb.Ad() @ [1, 2, 3, 1, 0, 0]


# # 3.1.3 incremental rotation

rotx(0.001)


R1 = np.eye(3,3);
R1cheap = np.eye(3,3);
w = np.r_[1, 0, 0]
dt = 0.01
for i in range(100):
   R1 = R1 @ trexp(skew(w*dt))
   R1cheap = R1cheap + R1cheap @ skew(w*dt)

np.linalg.det(R1) - 1
np.linalg.det(R1cheap) - 1

tr2angvec(trnorm(R1))
tr2angvec(trnorm(R1cheap))

# # 3.2.1 dynamics of moving bodies

J = np.array([[2, -1, 0], [-1, 4, 0], [0, 0, 3]])

dt = 0.05

def attitude():
   attitude = UnitQuaternion()
   w = 0.2 * np.r_[1, 2, 2].T
   for t in np.arange(0, 10, dt):
      wd =  -np.linalg.inv(J) @ (np.cross(w, J @ w))
      w += wd * dt
      attitude.increment(w * dt)
      yield r2t(attitude.R)

tranimate(attitude())

# # 3.2.2 transforming forces/torques
# wrench example

aW = aTb.inv().Ad().T @ [1, 2, 3, 0, 0, 0]

# # 3.3 smooth 1D trajectories

traj = tpoly(0, 1, np.linspace(0, 1, 50))
traj.plot()

traj2 = tpoly(0, 1, np.linspace(0, 1, 50), 10, 0)
traj2.plot()

np.mean(traj.qd) / np.max(traj.qd)

traj = lspb(0, 1, np.linspace(0, 1, 50))
traj.plot()

np.mean(traj.qd) / np.max(traj.qd)

traj = lspb(0, 1, np.linspace(0, 1, 50), 1.2)
traj = lspb(0, 1, np.linspace(0, 1, 50), 2)

np.max(traj.qd)

# # 3.3.2 multi-dimensional case

q = mtraj(lspb, [0, 2], [1, -1], 50)
qplot(q.q, block=False)

T = SE3.Rand()
q = np.r_[T.t, T.rpy()]

## 3.3.3 multi-segment trajectoreis
via = SO2(30, unit='deg') * np.array([[-1, 1, 1, -1, -1], [1, 1, -1, -1, 1]])

traj0 = mstraj(via.T, dt=0.2, tacc=0, qdmax=[2, 1])

plt.plot(traj0.q[:,0], traj0.q[:,1])

traj2 = mstraj(via.T, dt=0.2, tacc=2, qdmax=[2, 1])


# HACK q0 = mstraj(via(:,[2 3 4 1])', [2,1], [], via(:,1)', 0.2, 0)
# HACK plot(q0[:,0], q0[:,1])

# HACK q2 = mstraj(via(:,[2 3 4 1])', [2,1], [], via(:,1)', 0.2, 2)

[len(traj0), len(traj2)]

## 3.3.4 interpotation of orientation
R0 = SO3.Rz(-1) * SO3.Ry(-1)
R1 = SO3.Rz(1) * SO3.Ry(1)

rpy0 = R0.rpy()
rpy1 = R1.rpy()
rpy = mtraj(tpoly, rpy0, rpy1, 50)
pose = SO3.RPY(rpy.q)
len(pose)
plotvol3(2); pose.animate()

q0 = UnitQuaternion(R0)
q1 = UnitQuaternion(R1)

# HACK
q = q0.interp(q1, 50)
len(q)
plotvol3(2); q.animate()

## 3.3.5 direction of rotation
q0 = UnitQuaternion.Rz(-2)
q1 = UnitQuaternion.Rz(2)
q = q0.interp(q1, 50)
q.animate()

q = q0.interp(q1, 50, shortest=True)
q.animate()

## 3.3.6 Cartesian motion
T0 = SE3([0.4, 0.2, 0]) * SE3.RPY([0, 0, 3])
T1 = SE3([-0.4, -0.2, 0.3]) * SE3.RPY([-pi/4, pi/4, -pi/2])


T0.interp(T1, 0.5)

Ts = T0.interp(T1, 50)

len(Ts)

Ts[0]

plotvol3(2)
Ts.animate()
P = Ts.t
P.shape
qplot(P)

rpy = Ts.rpy()
qplot(rpy)


Ts = T0.interp(T1,lspb(0, 1, 50).q)
Ts = ctraj(T0, T1, 50)


# # 3.4.1.2 estimating orientation

from imu_data import IMU
true, imu = IMU()

attitude = UnitQuaternion()
for w in true.omega[:-1]:
   attitude.append(attitude[-1] * UnitQuaternion.EulerVec(w*true.dt))

print(attitude[99])
attitude.animate(true=imu.t)

plt.clf()
plt.plot(true.t, attitude.rpy())

## 3.4.4 sensor fusion
from imu_data import IMU
true, imu = IMU()
t = imu.t
o𝜉b = UnitQuaternion()
for ωm in imu.gyro[:-1]:
   o𝜉b.append(o𝜉b[-1] * UnitQuaternion.EulerVec(ωm * imu.dt))

plt.clf()
plt.plot(o𝜉b.rpy())
plt.title('naive')
plt.figure()
plt.plot(true.attitude.rpy())
plt.title('true')
plt.figure()
plt.plot(t, o𝜉b.angdist(true.attitude, metric=1), 'r' )

kI = 0.2
kP =1

b = np.zeros(imu.gyro.shape)  # initial bias
o𝜉b_ECF = UnitQuaternion()

for k, (ωm, am, mm) in enumerate(zip(imu.gyro[:-1], imu.accel[:-1], imu.magno[:-1])):
   b𝜉o = o𝜉b_ECF[-1].inv()
   σR = np.cross(am, b𝜉o * true.g) + np.cross(mm, b𝜉o * true.B)
   ωp = ωm - b[k,:] + kP * σR
   o𝜉b_ECF.append(o𝜉b_ECF[k] * UnitQuaternion.EulerVec(ωp * imu.dt))
   b[k+1,:] = b[k,:] - kI * σR * imu.dt

plt.plot(t, o𝜉b_ECF.angdist(true.attitude, metric=1), 'b')
plt.xlim(0, 20)
plt.ylim(0, 0.8)
plt.legend('Naive integration', 'ECF')

plt.figure()
plt.plot(t, b)
plt.show(block=True)
