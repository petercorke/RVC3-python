#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt
from numpy.core.shape_base import block
from numpy.lib.function_base import blackman

import sys
from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE3, SO2, SO3, UnitQuaternion
from rvcprint import rvcprint

# load the simulation data
from imu_data import IMU
true, imu = IMU()
t = imu.t
orientation = UnitQuaternion()
for i, w in enumerate(imu.gyro[:-1]):
   orientation.append(orientation[-1] * UnitQuaternion.EulerVec(w * imu.dt))

# plt.clf()
# plt.plot(orientation.rpy())
# plt.title('naive')
# plt.figure()
# plt.plot(true.orientation.rpy())
# plt.title('true')
# plt.figure()
# plt.plot(t, orientation.angdist(true.orientation, metric=0), 'r' )
# plt.show(block=True)

kI = 0.2
kP = 1

bias = np.zeros(imu.gyro.shape)  # initial bias
orientation_ECF = UnitQuaternion()

for k, (wm, am, mm) in enumerate(zip(imu.gyro[:-1], imu.accel[:-1], imu.magno[:-1])):
   invq = orientation_ECF[-1].inv()
   q = orientation_ECF[-1]
   sigmaR = np.cross(invq*am, true.g) + np.cross(invq*mm, true.B)
   wp = wm - bias[k,:] + kP * sigmaR
   orientation_ECF.append(orientation_ECF[k] * UnitQuaternion.EulerVec(wp * imu.dt))
   bias[k+1,:] = bias[k,:] - kI * sigmaR * imu.dt

ax = plt.subplot(211)
plt.plot(t, orientation.angdist(true.orientation), 'r' )
plt.plot(t, orientation_ECF.angdist(true.orientation), 'b')

ax.set_xlim(0, 20)
plt.ylabel('Orientation error (rad)')
plt.legend(['Simple integration', 'Explicit complementary filter'], loc='upper left')
plt.grid(True)

ax = plt.subplot(212)

plt.plot(t, bias)
ax.set_xlim(0, 20)
plt.xlabel('Time (s)')
plt.ylabel('Estimated gyro bias (rad/s)')
plt.legend(['$b_x$', '$b_y$', '$b_z$'], loc='center right')
plt.grid(True)

q1=UnitQuaternion.Rx(pi/2) 
q2=UnitQuaternion()
print(q1.angdist(q2, metric=2))

rvcprint()
