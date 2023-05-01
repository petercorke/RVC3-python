#! /usr/bin/env python

"""
Creates Fig 16.6
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

from pathlib import Path
from machinevisiontoolbox import *
from roboticstoolbox import *

from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt
from math import pi


sim = BDSim(animation=True)  # debug='i')
bd = sim.blockdiagram()
sim.set_options(animation=True)
clock = bd.clock(0.1, unit="s")

# wide angle camera
camera = CentralCamera.Default(f=0.002)

# camera optical axis is upward
T_B_C = SE3(0.2, 0.1, 0.3)

# landmark points on the ceiling
P = np.array([[0, 1, 3], [0, -1, 3]]).T

# desired landmark position on the image plane
pd = camera.project_point(P, pose=SE3(-2, 0, 0) * T_B_C)

q0 = [-6, 2, 0.6]
lmbda = 1


def plot_init(camera):
    camera.plot_point(pd, "b*")


def world_init(ax):
    # plot X, Y coords of world points
    ax.plot(P[0, :], P[1, :], "b*")


# load the bdsim model
model = Path(__file__).parent / "IBVS-holonomic.bd"
bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd)
out = sim.run(bd, 10)
print(out)
