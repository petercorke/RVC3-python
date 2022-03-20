#! /usr/bin/env python3
# fig 8.6

from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560
from roboticstoolbox import xplot
import bdsim
import rvcprint
import matplotlib.pyplot as plt

sim = bdsim.BDSim(hold=False)
bd = sim.blockdiagram()

clock = bd.clock(100, 'Hz')
puma = Puma560()
q0 = [0, pi/4, pi, 0, pi/4, 0]

# define the blocks
jacobian = bd.JACOBIAN(robot=puma, frame='0', inverse=True, name='Jacobian')
velocity = bd.CONSTANT([0, 0.05, 0, 0, 0, 0])
qdot = bd.PROD('**', matrix=True)
integrator = bd.DINTEGRATOR(clock, x0=q0, name='q')
robot = bd.ARMPLOT(robot=puma, q0=q0, name='plot')
# robot = bd.PRINT('{:.3f}')

# connect the blocks
bd.connect(jacobian, qdot[0])
bd.connect(velocity, qdot[1])
bd.connect(qdot, integrator)
bd.connect(integrator, jacobian, robot)

bd.compile()
bd.report_summary()

out = sim.run(bd, 5, dt=0.1)  # simulate for 5s
print(out)

# t = out.t
# x = out.x

t = out.clock0.t
x = out.clock0.x

xplot(t, x[:,:3], stack=True, color='k')

rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

Tfk = puma.fkine(x)
ax = xplot(t, Tfk.t, stack=True, labels='x y z', color='k')

from matplotlib.ticker import ScalarFormatter

y_formatter = ScalarFormatter(useOffset=True, useMathText=True)
ax[0].yaxis.set_major_formatter(y_formatter)

y_formatter = ScalarFormatter(useOffset=True, useMathText=True)
ax[2].yaxis.set_major_formatter(y_formatter)

# raise first 2 plots slightly
for a in ax[:2]:
    pos = list(a.get_position().bounds)  # x0 y0 width height 
    pos[1] = pos[1] + 0.03
    a.set_position(pos)

rvcprint.rvcprint(subfig='b')
dt = np.diff(out.t)
print("dt:", dt.min(), dt.max(), dt.mean())