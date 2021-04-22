from roboticstoolbox import *
import matplotlib.pyplot as plt
from spatialmath import base
import rvcprint

# puma = models.DH.Puma560()
# puma.plot(puma.qz, backend='pyplot')

robot = models.DH.IRB140()
S, T0 = robot.twists()
S 
S.exp(robot.qr).prod() * T0

robot.plot(robot.qz, limits=[-0.1, 0.5, -0.3, 0.3, -0.1, 0.5])

tw = S.exp(robot.qr)


lines = S.line()
lines.plot('k--', lw=2)


rvcprint.rvcprint(thicken=None)