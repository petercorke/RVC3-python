#! /usr/bin/env python

"""
Creates Fig 8.5
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import bdsim
from math import pi, sin, cos
import numpy as np
from roboticstoolbox.models.DH import Puma560
from spatialmath import SE3

sim = bdsim.BDSim()
bd = sim.blockdiagram()

clock = bd.clock(100, "Hz")
puma = Puma560()

# define the blocks

# q0 = [0, pi/4, pi, 0, pi/4, 0]

Te = SE3([0.6, -0.2, 0.7]) * SE3.Ry(np.pi)
sol = puma.ikine_a(Te)

q0 = sol.q

r = 0.05
T = 5.0
cc = Te.t
Kp = 8
# def circle(t):
#     x = r * np.cos(t / T * 2 * pi) + cc[0]
#     y = r * np.sin(t / T * 2 * pi) + cc[1]
#     return SE3(x, y, cc[2]) * SE3.Ry(pi)
# goal = bd.FUNCTION(circle)

# time = bd.TIME()
# bd.connect(time, goal)

goal = bd.CIRCLEPATH(radius=r, centre=cc, frequency=1 / T, unit="rps", pose=SE3.Ry(pi))
delta = bd.TR2DELTA()
jacobian = bd.JACOBIAN(robot=puma, frame="e", inverse=True, name="Jacobian")
gain = bd.GAIN(Kp)
qdot = bd.PROD("**", matrix=True)
integrator = bd.DINTEGRATOR(clock, x0=q0, name="q")
fkine = bd.FKINE(puma)
robot = bd.ARMPLOT(robot=puma, q0=q0, name="plot")
tr2t = bd.TR2T()
scope = bd.SCOPEXY(scale=[0.5, 0.7, -0.3, -0.10])
scope_norm = bd.SCOPE()
norm = bd.NORM()

# connect the blocks
bd.connect(goal, delta[1])
bd.connect(delta, qdot[1])

bd.connect(qdot, gain)
bd.connect(gain, integrator)
bd.connect(integrator, robot, fkine, jacobian)
bd.connect(fkine, delta[0], tr2t)
bd.connect(tr2t[0], scope[0])
bd.connect(tr2t[1], scope[1])
bd.connect(jacobian, qdot[0])

bd.connect(delta, norm)
bd.connect(norm, scope_norm)

bd.compile()

sim.report(bd)
out = sim.run(bd, 5, minstepsize=1e-6)  # simulate for 5s
