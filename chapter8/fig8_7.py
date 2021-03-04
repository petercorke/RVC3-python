# fig 8.7

import bdsim.simulation as sim
from math import pi, sin, cos
import numpy as np
from roboticstoolbox.models import Puma560

bd = sim.Simulation()

puma = Puma560()

# define the blocks

r = 1
T = 5
def circle(t):
    x = r * np.cos(t / T * 2 * pi) + x0
    y = r * np.sin(t / T * 2 * pi) + x0
    return SE3(x, y, 0)

time = BD.TIME()
goal = bd.FUNCTION(circle)
delta = bd.TR2DELTA()
jacobian = bd.JACOBIAN(puma)
inverse = bd.FUNCTION(lambda x: np.linalg.inv(x))
velocity = bd.CONSTANT([0, 0.5, 0, 0, 0, 0])
gain = bd.GAIN(5)
qdot = bd.PRODUCT(inverse, velocity)
integrator = bd.DINTEGRATOR(x0=[0, pi/4, pi, 0, pi/4, 0])
robot = bd.FKINE(puma)

# connect the blocks
bd.connect(time, goal)
bd.connect(goal, delta[1])
bd.connect(velocity, qdot[1])
bd.connect(qdot, integrator)
bd.connect(integrator, robot, jacobian)
bd.connect(jacobian, inverse)
bd.connect(inverse, qdot[0])

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires
bd.run(5)  # simulate for 5s
bd.dotfile('bd1.dot')  # output a graphviz dot file
bd.savefig('pdf')      # save all figures as pdf
bd.done()


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