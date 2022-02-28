#! /usr/bin/env python3

from numpy.core.shape_base import block
from roboticstoolbox import quintic
import matplotlib.pyplot as plt
import numpy as np
from rvcprint import rvcprint

traj = quintic(0, 1, np.linspace(0, 1, 50))
traj.plot()
rvcprint(subfig='a', thicken=1)

np.mean(traj.qd) / np.max(traj.qd)

traj = quintic(0, 1, np.linspace(0, 1, 50), 10, 0)
traj.plot()
rvcprint(subfig='b', thicken=1)
