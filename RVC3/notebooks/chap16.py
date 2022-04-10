# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import cv2 as cv

import ansitable
ansitable.options(unicode=True)

from spatialmath import *
from spatialmath.base import *
BasePoseMatrix._color=False
from roboticstoolbox import *

from spatialmath.base import *
import math
from math import pi

from machinevisiontoolbox import *
from machinevisiontoolbox.base import *

np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)
cv.setRNGSeed(0)

# ------------------------------ #


# XY/Z-Partitioned IBVS

%run -m IBVS-partitioned-main -H

# IBVS Using Polar Coordinates

camera = CentralCamera.Default(pose=SE3.Tz(-2)*SE3.Rz(pi))
P = mkgrid(2, 0.5, pose=SE3.Tz(2))
ibvs = IBVS_polar(camera, lmbda=0.1, P=P, pose_d=SE3.Tz(1), depth=2, graphics=False)
ibvs.run()
ibvs.plot_p()
ibvs.plot_pose()

# IBVS for a Spherical Camera

camera = SphericalCamera(pose=SE3.Trans(0.3, 0.3, -2)*SE3.Rz(0.4))
P = mkgrid(2, side=1.5, pose=SE3.Tz(0.5))
ibvs = IBVS_sph(camera, P=P, pose_d=SE3.Tz(-1.5), verbose=False, graphics=False)
ibvs.run()

# Applications


# Arm-Type Robot

%run -m IBVS-arm-main -H
plt.plot(out.clock1.t, out.clock1.x)

# Mobile Robot


# Holonomic Mobile Robot

camera = CentralCamera.Default(f=0.002);
T_B_C = SE3.Trans(0.2, 0.1, 0.3) * SE3.Rx(-pi/4);
P = np.array([[0, 1, 2], [0, -1, 2]]).T;
%run -m IBVS-holonomic-main -H

# Nonholonomic Mobile Robot

%run -m IBVS-nonholonomic-main -H

# Aerial Robot

%run -m IBVS-quadrotor-main -H

# Wrapping Up


# Further Reading


# Resources


# Exercises

