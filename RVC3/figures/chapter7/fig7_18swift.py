#!/usr/bin/env python3

from roboticstoolbox import *
from spatialmath import SE3
from roboticstoolbox.backends.Swift import Swift

robots = []  # list of robots
d = 1  # robot spacing
be = Swift()

be.launch()

for i in range(4):
    base = SE3(d * (i % 2), d * (i // 2), 0.0)  # place them on grid
    print(base)
    robot = models.URDF.Puma560()
    robot.base = base
    be.add(robot)
    robots.append(robot)

be.hold()
# T = p560.fkine(p560.qn)

# for i, c in enumerate(['run', 'rdn', 'lun', 'ldn']):
#     sol = p560.ikine_a(T, c)
#     print(sol)

#     robot[i].q = sol.q

# be.step()

# save the scene