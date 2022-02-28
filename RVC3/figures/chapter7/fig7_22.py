#!/usr/bin/env python3

import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath import *
import matplotlib.pyplot as plt
import numpy as np

puma = models.DH.Puma560()

TE1 = SE3(0.5, -0.3, 1.12) * SE3.Ry(pi/2);
TE2 = SE3(0.5, 0.3, 1.12) * SE3.Ry(pi/2);
t = np.arange(0, 2, 0.02);

Ts = ctraj(TE1, TE2, t);

sol = puma.ikine_a(Ts, 'lu');
xplot(t, sol.q, wrist=True, unwrap=True)

rvcprint.rvcprint(subfig='a')
#----------------------------------------------------------------------- #

# numeric inverse kinematics
soln = puma.ikine_LM(Ts);
xplot(t, soln.q, wrist=True, unwrap=True, loc='lower left')

rvcprint.rvcprint(subfig='b')
#----------------------------------------------------------------------- #

# joint space
sol1 = puma.ikine_a(TE1, 'lu');
sol2 = puma.ikine_a(TE2, 'lu');
traj = jtraj(sol1.q, sol2.q, t);
xplot(t, traj.q, wrist=True, unwrap=True, loc='lower left')

rvcprint.rvcprint(subfig='c')
#----------------------------------------------------------------------- #

# manipulability
m = puma.manipulability(sol.q);  # analytic
mn = puma.manipulability(soln.q);  # numerical

plt.clf()
plt.plot(t, m)
plt.plot(t, mn)
plt.ylabel('Manipulability')
plt.xlabel('Time (s)')
plt.legend(['Analytic IK', 'Numeric IK'], loc='lower right')

rvcprint.rvcprint(subfig='d')
