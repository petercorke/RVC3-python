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


# Wheeled Mobile Robots


# Car-Like Mobile Robots

%run -m lanechange -H
out
plt.plot(out.t, out.x);  # q vs time
plt.plot(out.x[:,0], out.x[:,1]);  # x vs y

# Driving to a Point

pgoal = (5, 5);
qs = (8, 5, pi / 2);
%run -i -m drivepoint -H
q = out.x;  # configuration vs time
plt.plot(q[:, 0], q[:, 1]);

# Driving along a Line

L = (1, -2, 4);
qs = (8, 5, pi / 2);
%run -i -m driveline -H

# Driving along a Path

%run -m drivepursuit -H

# Driving to a Configuration

qg = (5, 5, pi / 2);
qs = (9, 5, 0);
%run -i -m driveconfig -H
q = out.x;  # configuration vs time
plt.plot(q[:, 0], q[:, 1]);

# Differentially-Steered Vehicle


# Omnidirectional Vehicle


# Aerial Robots

%run -m quadrotor -H
t = out.t; x = out.x;
x.shape
plt.plot(t, x[:, 0], t, x[:, 1]);

# Advanced Topics


# Nonholonomic and Under-Actuated Systems


# Wrapping Up


# Further Reading

veh = Bicycle(speed_max=1, steer_max=np.deg2rad(30));
veh.q
veh.step([0.3, 0.2])
veh.q
veh.deriv(veh.q, [0.3, 0.2])

# Exercises

