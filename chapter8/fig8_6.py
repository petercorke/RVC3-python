# fig 8.6

from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560
from roboticstoolbox import qplot
import bdsim
import rvcprint
import matplotlib.pyplot as plt

sim = bdsim.BDSim()
bd = sim.blockdiagram()

puma = Puma560()
q0 = [0, pi/4, pi, 0, pi/4, 0]

# define the blocks
clock = bd.clock(0.05)
print(clock)
jacobian = bd.JACOBIAN(robot=puma, frame='0', inverse=True, name='Jacobian')
velocity = bd.CONSTANT([0, 0.05, 0, 0, 0, 0])
qdot = bd.PROD('**', matrix=True)
integrator = bd.DINTEGRATOR(clock=clock, x0=q0, name='q')
robot = bd.ARMPLOT(robot=puma, q0=q0, name='plot')
# robot = bd.PRINT('{:.3f}')

# connect the blocks
bd.connect(jacobian, qdot[0])
bd.connect(velocity, qdot[1])
bd.connect(qdot, integrator)
bd.connect(integrator, jacobian, robot)

bd.compile()
bd.report()

out = sim.run(bd, 5, minstepsize=1e-6)  # simulate for 5s

# qplot(out.t, out.x[:,:3], stack=True)

# rvcprint.rvcprint(subfig='b')

x = np.array(clock.x)
Tfk = puma.fkine(x)
ax = qplot(out.t, Tfk.t, stack=True, labels='x y z')

from matplotlib.ticker import ScalarFormatter

y_formatter = ScalarFormatter(useOffset=True, useMathText=True)
ax[2].yaxis.set_major_formatter(y_formatter)

# raise first 2 plots slightly
for a in ax[:2]:
    pos = list(a.get_position().bounds)  # x0 y0 width height 
    pos[1] = pos[1] + 0.03
    a.set_position(pos)

rvcprint.rvcprint(subfig='a')