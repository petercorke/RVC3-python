import numpy as np
import matplotlib.pyplot as plt
from math import pi, sqrt
from numpy.core.shape_base import block
from numpy.lib.function_base import blackman

from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE3, SO2, SO3, UnitQuaternion

# load the simulation data
from ex_tumble import tumble

data = tumble()
t = data.t
dt = 0.05

# do a naive integration of angular velocity to estimate attitude
attitude_naive = UnitQuaternion()
for w in data.gyro[:-1]:
   attitude_naive.append(attitude_naive[-1] * UnitQuaternion.EulerVec(w * dt))
#    print(attitude_naive[-1])
#    print(w)
print(attitude_naive[-1])
plt.clf()
plt.plot(attitude_naive.rpy())
plt.plot(data.attitude_true.rpy())

# plt.figure()
# plt.plot(t, attitude_naive.angdist(data.attitude_true, metric=2), 'r' )


# do the ECF to better estimate attitude

kI = 0.2
kP = 1

bias = np.zeros(data.gyro.shape)  # initial bias
attitude_ECF = UnitQuaternion()

for k, (wm, am, mm) in enumerate(zip(data.gyro[:-1], data.accel[:-1], data.magno[:-1])):
   invq = attitude_ECF[k].inv()
   sigmaR = np.cross(am, invq * data.g) + np.cross(mm, invq * data.B)
   wp = wm - bias[k,:] + kP * sigmaR
   attitude_ECF.append(attitude_ECF[k] * UnitQuaternion.EulerVec(wp * dt))
   bias[k+1,:] = bias[k,:] - kI * sigmaR * dt

ax = plt.subplot(211)
plt.plot(t, attitude_naive.angdist(data.attitude_true, metric=2), 'r' )
plt.plot(t, attitude_ECF.angdist(data.attitude_true, metric=2), 'b')
ax.set_xlim(0, 20)
plt.ylabel('Orientation error (rad)')
plt.legend(['Naive integration', 'ECF'], loc='upper left')
plt.grid(True)

ax = plt.subplot(212)
plt.plot(t, bias)
ax.set_xlim(0, 20)
plt.xlabel('Time (s)')
plt.ylabel('Estimated gyro bias b (rad/s)')
plt.legend(['b_x', 'b_y', 'b_z'], loc='upper left')
plt.grid(True)

q1=UnitQuaternion.Rx(pi/2)
q2=UnitQuaternion()
print(q1.angdist(q2, metric=2))

plt.show(block=True)


# clf
# clf
# subplot(211)
# plot(t, angle(attitude, truth), 'r', 'LineWidth', 2 );
# hold on
# plot(t, angle(attitude_ecf, truth), 'b', 'LineWidth', 2 );
# legend('standard', 'extended comp. filter', 'Location', 'NorthWest')
# grid on
# xlabel('Time (s)')
# ylabel('Orientation error (rad)')

# subplot(212)
# plot(t, b, 'LineWidth', 2)
# grid on
# xlabel('Time (s)')
# ylabel('Estimated gyro bias b (rad/s)')
# legend('b_x', 'b_y', 'b_z', 'Location', 'NorthWest')

# rvcprint