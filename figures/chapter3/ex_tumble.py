# Simulate the motion of a tumbling body
# 
# wm gyro measured (3xN)
# am accelerometer measured (3xN)
# mm magnetometer measured (3xN)
#
# g0 unit vector in direction of gravity in inertial frame
# m0 unit vector in direction of magnetic field in inertial frame
#
# qtrue true attitude as quaternion (1xN)

## vectorial sensor data

from collections import namedtuple
import numpy as np
from numpy.core.shape_base import block
from scipy.integrate import odeint
from spatialmath.base import unitvec
from spatialmath import UnitQuaternion

import matplotlib.pyplot as plt

def tumble():
    # accelerometer
    g0 = unitvec( [0, 0, 9.8] ).T
    gbias = 0.02 * np.r_[2, -2, 2].T  # bias 2% of norm

    # magnetometer, use N E U data in nT  for Brisbane
    m0 = unitvec( np.r_[28067.5, -5439.4, 44800.5] * 1e-9).T
    mbias = 0.02 * np.r_[-1, -1, 2]   # bias 2# of norm

    # gyro
    wbias = 0.05 * np.r_[-1, 2, -1] # bias 5% of max

    ## simulation

    #parameters
    dt = 0.05

    # make an asymmetric mass
    J = np.diag([2, 2, 2])
    J = np.diag([2, 4, 3])
    J[0,1] = -1
    J[1,0] = -1
    J[0,2] = -2
    J[2,0] = -2
    #eig(J)

    # initial condition
    w0 = 0.2 * np.r_[1, 2, 2].T

    # Solve Euler's rotational dynamics to get omega
    # 1 row per timestep
    t = np.arange(0, 20, dt)
    omega = odeint( lambda w, t:  -np.linalg.inv(J) @ np.cross(w, J @ w),
        w0, t) 

    # Solve for simulated sensor readings and true attitude
    # 1 column per timestep
    am = np.zeros(omega.shape)
    mm = np.zeros(omega.shape)

    truth = UnitQuaternion()

    for k, w in enumerate(omega):
        iq = truth[k].inv()
        am[k,:] = iq * g0 + gbias  # sensor reading in body frame
        mm[k,:] = iq * m0 + mbias  # sensor reading
        truth.append(truth[k] * UnitQuaternion.EulerVec(w * dt))
    del truth[-1]
    # add bias to measured 
    wm = omega + wbias

    data = namedtuple('tumble', 't omega_true attitude_true g B gyro accel magno')
    return data(t, omega, truth, g0, m0, wm, am, mm)

if __name__ == "__main__":

    def plot(t, y, title):
        plt.figure()
        plt.plot(t, y)
        plt.grid(True)
        plt.title(title)

    data = tumble()

    print(data.attitude_true[100])
    print(data.attitude_true[100].rpy())

    plot(data.t, data.attitude_true.rpy(), 'attitude')
    plot(data.t, data.gyro, 'gyro')
    plot(data.t, data.accel, 'accel')
    plot(data.t, data.magno, 'magno')

    plt.show(block=True)