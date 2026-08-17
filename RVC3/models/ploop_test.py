#! /usr/bin/env python

"""
Creates Fig 9.13
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import site
import numpy as np
import bdsim

from roboticstoolbox import quintic_func

site.addsitedir("bdsim")

from ploop import ploop, G

# test harness
sim = bdsim.BDSim()
bd = sim.blockdiagram()

# position = bd.quintic(0) HACK

quinticfunc = quintic_func(0, 1, 1)
trajectory = bd.FUNCTION(quinticfunc, nout=3, name="quintic")
time = bd.TIME()

taud = bd.CONSTANT(20 / G)
# speed = bd.WAVEFORM(wave='triangle', freq=2, amplitude=25)
PLOOP = bd.SUBSYSTEM(ploop, name="PLOOP")
theta_scope = bd.SCOPE(nin=2, name=r"$\theta$", labels=["actual", "demand"])
werr_scope = bd.SCOPE(name=r"$\omega$ error")
tau_scope = bd.SCOPE(name=r"$\tau$")
wff_scope = bd.SCOPE(name=r"$\omega_{ff}$")

bd.connect(time, trajectory)
bd.connect(trajectory[0], PLOOP[0], theta_scope[1])
bd.connect(trajectory[1], PLOOP[1], wff_scope)
bd.connect(taud, PLOOP[2])
bd.connect(PLOOP[0], theta_scope[0])

bd.connect(PLOOP[2], werr_scope)
bd.connect(PLOOP[3], tau_scope)

bd.compile()  # check the diagram


if __name__ == "__main__":
    sim.report(bd)
    out = sim.run(bd, 1, dt=1e-3)
