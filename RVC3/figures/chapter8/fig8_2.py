


"""
@author Jesse Haviland
"""

import swift
import roboticstoolbox as rtb
import spatialgeometry as sg
import spatialmath as sm

r = rtb.models.UR5()
r.base = sm.SE3(0.1, 0.1, 0.0)
r.q = [0, -1.1, 1.4, -0.6, 0.4, 0.4]

env = swift.Swift()
env.launch()
env.set_camera_pose([0.4, 1, 0.5], [0.4, 0, 0.5])
env.add(r, robot_alpha=0.4)

axes = []

for link in r:
    if link.isjoint:
        axes.append(sg.Axes(0.08, base=r.fkine(r.q, end=link)))
        env.add(axes[-1])


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

rvcprint.rvcprint(thicken=None)