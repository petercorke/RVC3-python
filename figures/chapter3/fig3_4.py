#! /usr/bin/env python3

from roboticstoolbox import trapezoidal, quintic, mtraj
import matplotlib.pyplot as plt
import numpy as np
from rvcprint import rvcprint

traj = mtraj(quintic, [0, 2], [1, -1], 50)
traj = mtraj(trapezoidal, [0, 2], [1, -1], 50)
plt.plot(traj.t, traj.q, '.-', markersize=6, linewidth=2)
plt.legend(['$q_0$', '$q_1$'])
plt.xlim(0, 50)
plt.xlabel('k (step)')
plt.ylabel('q')
plt.grid(True)

rvcprint()