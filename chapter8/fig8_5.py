# fig 8.5

from math import pi
import numpy as np
from roboticstoolbox.models import Puma560

import bdsim

bd = bdsim.BlockDiagram(debug='s')

puma = Puma560()
q0 = [0, pi/4, pi, 0, pi/4, 0]

# swift = puma.plot(q0, block=False)

# def update(q):
#     global puma, swift

#     puma.q = q
#     swift.step()

# define the blocks
jacobian = bd.FUNCTION(lambda q: puma.jacob0(q), name='Jacobian')
inverse = bd.FUNCTION(lambda x: np.linalg.inv(x), name='inv')
velocity = bd.CONSTANT([0, 0.5, 0, 0, 0, 0])
qdot = bd.PROD('**', matrix=True)
integrator = bd.INTEGRATOR(x0=q0)
# robot = bd.FUNCTION(update, name='plot')
# robot = bd.PRINT('{:.3f}')

# connect the blocks
inverse[0] = jacobian
qdot[0] = inverse
qdot[1] = velocity
integrator[0] = qdot
jacobian[0] = integrator
robot[0] = integrator

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
bd.run(5)  # simulate for 5s
# bd.dotfile('bd1.dot')  # output a graphviz dot file
# bd.savefig('pdf')      # save all figures as pdf
bd.done()

"""
[A] -> bd.JACOBIAN(puma)          -> bd.PRODUCT('**') -> bd.DINTEGRATOR(x0=[0, pi/4, pi, 0, pi/4, 0]) -> bd.ROBOTPLOT(puma, backend='swift')
bd.CONSTANT([0, 0.5, 0, 0, 0, 0]) -> 
                                                                                                        -> [A]

"""