#! /usr/bin/env python

from pathlib import Path
from machinevisiontoolbox import *
from bdsim import Clock, bdload, BDSim
from spatialmath import SE3, Polygon2
from spatialmath.base import angdiff
from math import atan2, sqrt
import matplotlib.pyplot as plt


sim = BDSim(animation=True)  # debug='i')
bd = sim.blockdiagram()

clock = bd.clock(0.1, unit="s")
camera = CentralCamera.Default()

pose_0 = SE3(1, 1, -3) * SE3.Rz(0.6)

model = Path(__file__).parent / "IBVS-partitioned.bd"
print(model)


def plot_init(camera):
    print("@@@@@plot_init")
    camera.plot_point(bd["p*"].value, "b*")


def rho_theta(p):
    A_d = 200
    theta_d = 0

    # square is 400x400

    rho = 1 - sqrt(Polygon2(p).area()) / A_d

    # this is the edge parallel to the x-axis
    theta = atan2(p[1, 2] - p[1, 1], p[0, 2] - p[0, 1])
    theta = angdiff(theta_d - theta)

    return np.r_[rho, theta]


bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd)
out = sim.run(bd, 150)
print(out)
