#! /usr/bin/env python

"""
Creates Fig 9.20
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path
from bdsim import BDSim, bdload
from roboticstoolbox.models.DH import Puma560

robot = Puma560().nofriction()

model = Path(__file__).parent / "feedforward.bd"

sim = BDSim(animation=True)
bd = sim.blockdiagram()
clock_ff = bd.clock(10, unit="Hz")
clock_fb = bd.clock(50, unit="Hz")

bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd, "summary")
out = sim.run(bd, 5, watch=["Joint space trajectory[0]"])
print(out)

import matplotlib.pyplot as plt

plt.plot(out.t, out.x[:, 1], out.t, out.y0[:, 1])
plt.show(block=True)
