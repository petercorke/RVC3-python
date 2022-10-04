# fig 8.5

from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560

import bdsim

sim = bdsim.BDSim()
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

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
out = sim.run(bd, 2, minstepsize=1e-6)  # simulate for 5s
# bd.dotfile('bd1.dot')  # output a graphviz dot file
# bd.savefig('pdf')      # save all figures as pdf
bd.done()

"""
[A] -> bd.JACOBIAN(puma)          -> bd.PRODUCT('**') -> bd.DINTEGRATOR(x0=[0, pi/4, pi, 0, pi/4, 0]) -> bd.ROBOTPLOT(puma, backend='swift')
bd.CONSTANT([0, 0.5, 0, 0, 0, 0]) -> 
                                                                                                        -> [A]

"""