from numpy.core.shape_base import block
from roboticstoolbox import tpoly
import matplotlib.pyplot as plt
import numpy as np

traj = tpoly(0, 1, np.linspace(0, 1, 50))
traj.plot()
# rvcprint('subfig', 'a', 'thicken', 1)
plt.show(block=True)

np.mean(traj.yd) / np.max(traj.yd)

traj = tpoly(0, 1, np.linspace(0, 1, 50), 10, 0)
traj.plot()
plt.show(block=True)
# rvcprint('subfig', 'b', 'thicken', 1)