#!/usr/bin/env python3

"""
Creates Fig 7.22
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import bdsim
from roboticstoolbox import *

sim = bdsim.BDSim(animation=True)
bd = sim.blockdiagram("forward kinematics")

puma = models.DH.Puma560()

_jtraj = bd.JTRAJ(q0=puma.qr, qf=puma.qz)
fk = bd.FKINE(puma)
rplot = bd.ARMPLOT(puma)
_transl = bd.TR2T()
xyplot = bd.SCOPEXY(name="XZ plane")

bd.connect(_jtraj.q, fk.q, rplot.q)
bd.connect(fk.T, _transl.T)
bd.connect(_transl.x, xyplot[0])
bd.connect(_translt.z, xyplot[1])

bd.compile()

sim.report(bd)
sim.run(bd, 10)
