# fig 9.20

import bdsim.simulation as sim
from math import pi
import numpy as np
from roboticstoolbox.models import Puma560

bd = sim.Simulation()

puma = Puma560()

# define the blocks

traj = bd.JTRAJ(qr, qz, 10)
torque_sum = bd.SUM('++')
fdyn = bd.FDYN(puma)
invdyn = bd.IDYN(puma)
plot = bd.ROBOTPLOT(puma, backend='swift')

q_err = bd.SUM('+-')
qd_err = bd.SUM('+-')
fb_sum = bd.SUM('++')

# connect the blocks
invdyn[0:2] = traj

q_err[0] = traj[0]
q_err[1] = fdyn[0]

qd_err[0] = traj[1]
qd_err[1] = fdyn[1]

fb_sum[0] = q_err * bd.GAIN(100, name='Kp')
fb_sum[1] = qd_err * bd.GAIN(5, name='Kd')

torque_sum[0] = fb_sum
torque_sum[1] = invdyn

fdyn[0] = torque_sum

plot[0] = fdyn[0]

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
bd.run(5)  # simulate for 5s
bd.dotfile('bd1.dot')  # output a graphviz dot file
bd.savefig('pdf')      # save all figures as pdf
bd.done()


"""
JTRAJ[0]  -0->o SUM('+-) -> GAIN(100)    -0->o SUM('++')  -0->o SUM('++') -> FDYN
FDYN[0]   -1->o

JTRAJ[1]  -0->o SUM('+-) -> GAIN(5)      -1->o  
FDYN[1]   -1->o

JTRAJ ==> IDYN                                            -1->o
"""