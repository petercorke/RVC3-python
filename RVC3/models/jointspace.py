#!/usr/bin/env python3

import bdsim
from roboticstoolbox import *

sim = bdsim.BDSim(verbose=True, animation=True)
bd = sim.blockdiagram('forward kinematics')

puma = models.DH.Puma560()

jtraj = bd.JTRAJ(q0=puma.qr, qf=puma.qz)
fk = bd.FKINE(puma)
rplot = bd.ARMPLOT(puma)
t = bd.TR2T()
xyplot = bd.SCOPEXY(name='XZ plane')

bd.connect(jtraj.q, fk.q, rplot.q)
bd.connect(fk.T, t.T)
bd.connect(t.x, xyplot[0])
bd.connect(t.z, xyplot[1])

bd.compile()
bd.report()

sim.run(bd, 10)
sim.done(bd, block=True)