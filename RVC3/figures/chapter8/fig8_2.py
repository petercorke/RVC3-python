#!/usr/bin/env python3


"""
@author Jesse Haviland
"""

import swift
import roboticstoolbox as rtb
import spatialgeometry as sg
import spatialmath as sm
from math import pi
import numpy as np

r = rtb.models.UR5()
#r.base = sm.SE3(0.1, 0.1, 0.0)
r.q = [0, -1.1, 1.4, -0.6, 0.4, 0.4]
r.q = [0, -pi/2, pi/2, 0, pi/2, 0]
print(r)

J = r.jacob0(r.q)
print(J)
print(np.linalg.det(J))
rtb.jsingu(J)

length = 0.6
env = swift.Swift()
env.launch()
env.set_camera_pose([length, 1, 0.5], [0.4, 0, 0.5])
env.add(r, robot_alpha=0.4)

axes = []

for link in r:
    if link.isjoint:
        # axes.append(sg.Axes(0.08, base=r.fkine(r.q, end=link)))
        joint = link.ets[-1]
        T = r.fkine(r.q, end=link)
        if joint.axis == "Rx":
            T *= sm.SE3.Ry(pi/2)
        elif joint.axis == "Ry":
            T *= sm.SE3.Rx(-pi/2)
        env.add(sg.Arrow(length=0.5, radius=0.005, color='red', pose=T* sm.SE3.Tz(-length/3)))


env.hold()


# puma = models.DH.Puma560()
# # puma.name = ''

# options = {
#     'robot': {'alpha': 0.5},
#     'shadow': {'alpha': 0.7},
#     'jointaxes': {'color': 'black'},
#     'jointlabels': {'size': 11},
# }
# puma.plot(puma.qn, jointlabels=True, name=False, backend='pyplot', options=options)

# rvcprint.rvcprint()