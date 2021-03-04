# fig 9.18

import bdsim.simulation as sim
from math import pi
import numpy as np
from roboticstoolbox.models import Puma560

bd = sim.Simulation()

puma = Puma560()

# define the blocks

torque = bd.CONSTANT([0, 0, 0, 0, 0, 0])
robot = bd.FDYN(puma)
plot = bd.ROBOTPLOT(puma, backend='swift')

# connect the blocks
robot[0] = torque
plot[0] = robot

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
bd.run(5)  # simulate for 5s
bd.dotfile('bd1.dot')  # output a graphviz dot file
bd.savefig('pdf')      # save all figures as pdf
bd.done()