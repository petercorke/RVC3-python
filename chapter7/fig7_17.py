import bdsim
from roboticstoolbox import *

sim = bdsim.BDSim(verbose=True, animation=True)
bd = sim.blockdiagram('forward kinematics')

puma = models.DH.Puma560()

jtraj = bd.JTRAJ(q0=puma.qr, qf=puma.qr)
fk = bd.FORWARD_KINEMATICS(puma)
rplot = bd.ARMPLOT(puma)
t = bd.TR2T()
xyplot = bd.SCOPEXY()

bd.connect(jtraj.q, fk.q, rplot.q)
bd.connect(fk.T, t.T)
# bd.connect(t[:2], xyplot[:2])
bd.connect(t.x, xyplot[0])
bd.connect(t.y, xyplot[1])

bd.compile()
bd.report()

sim.run(bd, 10)