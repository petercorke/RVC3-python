#!/usr/bin/env python3

from roboticstoolbox import *
import matplotlib.pyplot as plt
from spatialmath import base
import rvcprint

# puma = models.DH.Puma560()
# puma.plot(puma.qz, backend='pyplot')

robot = models.DH.IRB140()
S, TE0 = robot.twists()
S 
S.SE3(robot.qr).prod() * TE0

robot.plot(robot.qz, limits=[-0.1, 0.5, -0.3, 0.3, -0.1, 0.5])

T = S.SE3(robot.qr).prod() * TE0


lines = S.line()
lines.plot('k--', lw=2)


rvcprint.rvcprint(thicken=None)