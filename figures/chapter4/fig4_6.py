#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from roboticstoolbox import *
from bdsim import *
import runpy

# lane change example

def bdload(path):

    dict = runpy.run_path(path)
    # g = globals()
    # for key in ['bd', 'sim', 'steering']:
    #     g[key] = dict[key]

    return dict['bd']

bd = bdload("models/lanechange.py")
bd.report()

sim = BDSim()
out = sim.run(bd, T=10, dt=0.01, watch=[bd["steering"]])

xplot(out.t, np.column_stack((out.x[:,1:], out.y0.reshape(-1,1))), stack=True, color='k', grid=True, labels=['y', r'$\theta$', r'$\gamma$'])
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

plt.figure()
plt.plot(out.x[:,0], out.x[:,1], color='k')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(0, 10)
plt.ylim(0, 1.2)
rvcprint.rvcprint(subfig='b')

