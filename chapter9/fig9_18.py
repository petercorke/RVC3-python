# fig 9.18

import bdsim
from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560

def PumaCollapse():
    bd = bdsim.BlockDiagram(name='Puma collapsing', graphics=False)

    puma = Puma560().nofriction()

    # define the blocks

    torque = bd.CONSTANT([0, 0, 0, 0, 0, 0])
    robot = bd.FOWARDDYNAMICS(robot=puma)
    plot = bd.ARMPLOT(puma)

    # connect the blocks
    bd.connect(torque, robot)
    bd.connect(robot[0], plot)

    bd.compile()   # check the diagram
    bd.report()    # list all blocks and wires
    out = bd.run(5)  # simulate for 5s

    bd.done()

    return out

if __name__ == "__main__":

    PumaCollapse()