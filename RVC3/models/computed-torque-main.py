#! /usr/bin/env python

"""
Creates Fig 9.21
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path
from bdsim import BDSim, bdload
from roboticstoolbox.models.DH import Puma560

robot = Puma560().nofriction()

model = Path(__file__).parent / "computed-torque.bd"

sim = BDSim(animation=True)
bd = sim.blockdiagram()
clock_fb = bd.clock(50, unit="Hz")

bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd, "summary")
out = sim.run(bd, 5)
print(out)
