from roboticstoolbox import mstraj, lspb
import matplotlib.pyplot as plt
import numpy as np
from spatialmath import SE3
from math import pi
from rvcprint import rvcprint

T0 = SE3(0.4, 0.2, 0) * SE3.RPY([0, 0, 3])
T1 = SE3(-0.4, -0.2, 0.3) * SE3.RPY([-pi/2, 0, -pi/2])

Ts = T0.interp(T1, lspb(0, 1, 50).y)

Ts[0]

# Ts.animate()

t = np.arange(0, 50)
plt.plot(t, Ts.t, '.-', linewidth=2, markersize=8)
plt.ylabel('position')
plt.xlabel('k (step)');
plt.grid(True)
plt.legend(['x', 'y', 'z'], loc='lower left')
plt.xlim(0,49)

rvcprint(subfig='a', thicken=1)

t = np.arange(0, 50)
plt.clf()
plt.plot(t, Ts.rpy(), '.-', linewidth=2, markersize=8)
plt.ylabel('RPY angles')
plt.xlabel('k (step)');
plt.grid(True)
plt.legend(['roll', 'pitch', 'yaw'], loc='lower left')
plt.xlim(0,49)

rvcprint(subfig='b', thicken=1)

