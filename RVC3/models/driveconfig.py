#!/usr/bin/env python3

"""
Creates Fig 4.14
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

# run with command line -a switch to show animation

from math import pi, sqrt, atan, atan2
import bdsim

sim = bdsim.BDSim(animation=True)
bd = sim.blockdiagram()

# parameters
xg = [5, 5, pi / 2]
Krho = bd.GAIN(1, name="Krho")
Kalpha = bd.GAIN(5, name="Kalpha")
Kbeta = bd.GAIN(-2, name="Kbeta")

xg = [5, 5, pi / 2]
x0 = [5, 2, 0]
x0 = [5, 9, 0]


# annotate the graphics
def background_graphics(ax):
    ax.plot(*xg[:2], "*")
    ax.plot(*x0[:2], "o")


# convert x,y,theta state to polar form
def polar(x, dict):
    rho = sqrt(x[0] ** 2 + x[1] ** 2)

    if not "direction" in dict:
        # direction not yet set, set it
        beta = -atan2(-x[1], -x[0])
        alpha = -x[2] - beta
        print("alpha", alpha)
        if -pi / 2 <= alpha <= pi / 2:
            dict["direction"] = 1
        else:
            dict["direction"] = -1
        print("set direction to ", dict["direction"])

    if dict["direction"] == -1:
        beta = -atan2(x[1], x[0])
    else:
        beta = -atan2(-x[1], -x[0])
    alpha = -x[2] - beta

    # clip alpha
    if alpha > pi / 2:
        alpha = pi / 2
    elif alpha < -pi / 2:
        alpha = -pi / 2

    return [
        dict["direction"],
        rho,
        alpha,
        beta,
    ]


# constants
goal0 = bd.CONSTANT([xg[0], xg[1], 0], name="goal_pos")
goalh = bd.CONSTANT(xg[2], name="goal_heading")

# stateful blocks
bike = bd.BICYCLE(x0=x0, vlim=2, slim=1.3, name="vehicle")

# functions
fabs = bd.FUNCTION(lambda x: abs(x), name="abs")
polar = bd.FUNCTION(
    polar,
    nout=4,
    persistent=True,
    name="polar",
    inames=("x",),
    onames=("direction", r"$\rho$", r"$\alpha$", r"$\beta"),
)
stop = bd.STOP(lambda x: x < 0.01, name="close enough")
steer_rate = bd.FUNCTION(lambda u: atan(u), name="atan")

# arithmetic
vprod = bd.PROD("**", name="vprod")
wprod = bd.PROD("**/", name="aprod")
xerror = bd.SUM("+-")
heading_sum = bd.SUM("++")
gsum = bd.SUM("++")

# displays
vplot = bd.VEHICLEPLOT(
    scale=[0, 10],
    size=0.7,
    shape="box",
    path="b:",
    init=background_graphics,
)
# movie="rvc4_11.mp4",)
ascope = bd.SCOPE(name=r"$\alpha$")
bscope = bd.SCOPE(name=r"$\beta$")

# connections

bd.connect(bike, vplot)
bd.connect(bike, xerror[0])
bd.connect(goal0, xerror[1])

bd.connect(xerror, polar)
bd.connect(polar[1], Krho, stop)  # rho
bd.connect(Krho, vprod[1])
bd.connect(polar[2], Kalpha, ascope)  # alpha
bd.connect(Kalpha, gsum[0])
bd.connect(polar[3], heading_sum[0])  # beta
bd.connect(goalh, heading_sum[1])
bd.connect(heading_sum, Kbeta, bscope)

bd.connect(polar[0], vprod[0], wprod[1])
bd.connect(vprod, fabs, bike.v)
bd.connect(fabs, wprod[2])
bd.connect(wprod, steer_rate)
bd.connect(steer_rate, bike.gamma)

bd.connect(Kbeta, gsum[1])
bd.connect(gsum, wprod[0])

bd.compile()

if __name__ == "__main__":

    sim.report(bd)
    out = sim.run(bd, T=10)
