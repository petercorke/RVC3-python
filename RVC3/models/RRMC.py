#! /usr/bin/env python

"""
Creates Fig 8.3
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560

import bdsim

sim = bdsim.BDSim()
bd = sim.blockdiagram()

clock = bd.clock(100, "Hz")
puma = Puma560()
q0 = [0, pi / 4, pi, 0, pi / 4, 0]

# define the blocks
jacobian = bd.JACOBIAN(robot=puma, frame="0", inverse=True, name="Jacobian")
velocity = bd.CONSTANT([0, 0.05, 0, 0, 0, 0])
qdot = bd.PROD("**", matrix=True)
integrator = bd.DINTEGRATOR(clock, x0=q0, name="q")
robot = bd.ARMPLOT(robot=puma, q0=q0, name="plot")
# robot = bd.PRINT('{:.3f}')

# connect the blocks
bd.connect(jacobian, qdot[0])
bd.connect(velocity, qdot[1])
bd.connect(qdot, integrator)
bd.connect(integrator, jacobian, robot)

bd.compile()  # check the diagram

sim.report(bd)
out = sim.run(bd, 2, minstepsize=1e-6)  # simulate for 5s
