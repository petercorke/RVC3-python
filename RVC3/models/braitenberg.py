#!/usr/bin/env python3

"""
Creates Fig 5.4
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import bdsim
import math
import numpy as np
from spatialmath import SE2


sim = bdsim.BDSim(animation=True, graphics=True)
bd = sim.blockdiagram()


def sensorfield(x, y):
    xc = 60
    yc = 90
    return 200 / ((x - xc) ** 2 + (y - yc) ** 2 + 200)


def background_graphics(ax):
    v = np.arange(0, 100)
    X, Y = np.meshgrid(v, v)
    Z = sensorfield(X, Y)
    a = ax.imshow(Z, cmap="viridis")
    ax.figure.colorbar(a)


speed = bd.CONSTANT(2, name="speed")
sum1 = bd.SUM("+--")
sum2 = bd.SUM("+-")

Kv = bd.GAIN(50, name="Kv")
Ks = bd.GAIN(5, name="Ks")
bike = bd.BICYCLE(x0=[5, 5, 0], speed_max=1, name="vehicle")


def sensorfunc(x, offset):
    xy = SE2(x) * offset
    return sensorfield(xy[0], xy[1])[0]


# offset = np.r_[0, 2]
leftsensor = bd.FUNCTION(sensorfunc, nin=1, fargs=([0, -2],), name="leftsensor")
rightsensor = bd.FUNCTION(sensorfunc, nin=1, fargs=([0, 2],), name="rightsensor")

vplot = bd.VEHICLEPLOT(
    scale=[0, 100],
    size=5,
    shape="box",
    trail=True,
    name="sensor field",
    init=background_graphics,
)
vscope = bd.SCOPE(name="velocity")
wscope = bd.SCOPE(name="steering rate")

bd.connect(bike, leftsensor, rightsensor, vplot)
bd.connect(rightsensor, sum1[1], sum2[0])
bd.connect(speed, sum1[0])
bd.connect(leftsensor, sum1[2], sum2[1])
bd.connect(sum1, Kv)
bd.connect(Kv, vscope, bike.v)

bd.connect(sum2, wscope, Ks)
bd.connect(Ks, bike.gamma)

bd.compile()

if __name__ == "__main__":
    sim.report(bd)
    out = sim.run(bd, T=125, dt=0.2)
