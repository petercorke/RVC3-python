#! /usr/bin/env python

"""
Creates Fig 9.8
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import numpy as np
import bdsim

import site
import numpy as np
import bdsim

from vloop import vloop, B


# test harness for velocity loop
sim = bdsim.BDSim(graphics=True, progress=False)
bd = sim.blockdiagram()

# parameters
disturbance = bd.CONSTANT(0, name="disturbance")
feedforward = bd.CONSTANT(0)
# speed = bd.WAVEFORM(wave='triangle', freq=2, amplitude=25)
speed = bd.INTERPOLATE(
    x=(0, 0.1, 0.3, 0.4, 0.6, 1), y=(0, 0, 50, 50, 0, 0), time=True, name="demand"
)

# import the velocity loop
VLOOP = bd.SUBSYSTEM(vloop, name="VLOOP")

# scopes
w_scope = bd.SCOPE(nin=2, name=r"$\omega$", labels=["actual", "demand"])
werr_scope = bd.SCOPE(name=r"$\omega_{err}$")
tau_scope = bd.SCOPE(name=r"$\tau$")
integral_scope = bd.SCOPE(name="integral")

demand_scope = bd.SCOPE(name="demand scope")

bd.connect(speed, demand_scope)

bd.connect(VLOOP[0], w_scope[0])
bd.connect(VLOOP[1], werr_scope)
bd.connect(VLOOP[2], tau_scope)
bd.connect(VLOOP[3], integral_scope)

bd.connect(disturbance, VLOOP[1])
bd.connect(speed, VLOOP[0], w_scope[1])
bd.connect(feedforward, VLOOP[2])

bd.compile()  # check the diagram

if __name__ == "__main__":
    sim.report(bd)

    out = sim.run(bd, 1, dt=1e-3)
