#! /usr/bin/env python3
# fig 8.7

import bdsim
from math import pi, sin, cos
import numpy as np
from roboticstoolbox.models.DH import Puma560
from spatialmath import SE3

sim = bdsim.BDSim(verbose=True)
bd = sim.blockdiagram()

puma = Puma560()

# define the blocks

q0 = [0, pi/4, pi, 0, pi/4, 0]

r = 0.05
T = 5
cc = puma.fkine(puma.qn).t
def circle(t):
    x = r * np.cos(t / T * 2 * pi) + cc[0]
    y = r * np.sin(t / T * 2 * pi) + cc[1]
    return SE3(x, y, cc[2]) * SE3.Ry(pi)

time = bd.TIME()
goal = bd.FUNCTION(circle)
delta = bd.TR2DELTA()
jacobian = bd.JACOBIAN(robot=puma, frame='e', inverse=True, name='Jacobian')
gain = bd.GAIN(2)
qdot = bd.PROD('**', matrix=True)
integrator = bd.INTEGRATOR(x0=q0, name='q')
fkine = bd.FKINE(puma)
robot = bd.ARMPLOT(robot=puma, q0=q0, name='plot')
tr2t = bd.TR2T()
scope = bd.SCOPEXY(scale=[0.5, 0.7, -0.25, -0.05])

# connect the blocks
bd.connect(time, goal)
bd.connect(goal, delta[1])
bd.connect(delta, qdot[1])

bd.connect(qdot, gain)
bd.connect(gain, integrator)
bd.connect(integrator, robot, fkine, jacobian)
bd.connect(fkine, delta[0], tr2t)
bd.connect(tr2t[0], scope[0])
bd.connect(tr2t[1], scope[1])
bd.connect(jacobian, qdot[0])


bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
out = sim.run(bd, 10, minstepsize=1e-6, dt=0.05)  # simulate for 5s
# bd.dotfile('bd1.dot')  # output a graphviz dot file
# bd.savefig('pdf')      # save all figures as pdf
bd.done(block=True)

"""
            [q] -> JACOB0(puma) -> INV  -> PROD('**') -> GAIN(5) -> integrator -> [q]
                FKINE(puma) -> T2XYZ[0:2] -> XYPLOT
                            => TRDELTA  =>
TIME() -> FUNCTION(circle)  => 


 integrator -> JACOB0(puma) -> INV        -0->o PROD('**') -> GAIN(5) -> integrator
 integrator -> FKINE(puma) --> T2XYZ[0:2] -> XYPLOT
                           +-0->o TRDELTA -1->o
TIME() -> FUNCTION(circle)  -1->o

parser  (REFERENCE | ARROW | TEE | BLOCK, arrowtype: arrow | tee, arrow id, indent, str)
"""