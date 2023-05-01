#! /usr/bin/env python

"""
Creates Fig 9.28
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path
import numpy as np
from bdsim import BDSim, bdload

obstacle_pos = 0.8
m1 = 0.5
m2 = 1
LQR = np.c_[169.9563, 62.9010, -19.9563, 71.1092].T
Ks = 5
force_lim = 2

model = Path(__file__).parent / "SEA.bd"

sim = BDSim(animation=True)
bd = sim.blockdiagram()

bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd, "summary")
out = sim.run(bd, 5, watch=["Clip Block", "Ks"])
print(out)
