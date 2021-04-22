from numpy.core.shape_base import block
from roboticstoolbox import tpoly
import matplotlib.pyplot as plt
import numpy as np
from rvcprint import rvcprint

traj = tpoly(0, 1, np.linspace(0, 1, 50))
traj.plot()
rvcprint(subfig='a', thicken=1)

np.mean(traj.yd) / np.max(traj.yd)

traj = tpoly(0, 1, np.linspace(0, 1, 50), 10, 0)
traj.plot()
rvcprint(subfig='b', thicken=1)
