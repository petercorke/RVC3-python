from roboticstoolbox import lspb, tpoly, mtraj
import matplotlib.pyplot as plt
import numpy as np
from rvcprint import rvcprint

traj = mtraj(tpoly, [0, 2], [1, -1], 50)
traj = mtraj(lspb, [0, 2], [1, -1], 50)
plt.plot(traj.x, traj.y, '.-', markersize=6, linewidth=2)
plt.legend(['q_1', 'q_2'])
plt.xlim(0, 50)
plt.xlabel('k (step)')
plt.ylabel('q')
plt.grid(True)

rvcprint()