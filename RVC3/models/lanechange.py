#!/usr/bin/env python3

"""
Creates Fig 4.5
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from bdsim import *

sim = BDSim()

bd = sim.blockdiagram()

speed = bd.CONSTANT(1, name="speed")
steering = bd.PIECEWISE((0, 0), (3, 0.5), (4, 0), (5, -0.5), (6, 0), name="steering")
vehicle = bd.BICYCLE(name="vehicle")
xyscope = bd.SCOPEXY1(indices=[0, 1], scale=[0, 10, 0, 1.2])
bd.connect(speed, vehicle.v)
bd.connect(steering, vehicle.gamma)
bd.connect(vehicle, xyscope)
bd.compile()

if __name__ == "__main__":
    sim.report(bd)
    out = sim.run(bd, T=10)
