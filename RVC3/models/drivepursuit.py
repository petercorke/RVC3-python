#!/usr/bin/env python3

"""
Creates Fig 4.11
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

# run with command line -a switch to show animation

import numpy as np
import math
import roboticstoolbox as rtb
import bdsim

# parameters for the path
look_ahead = 5
speed = 1
dt = 0.1
tacc = 1
x0 = [2, 2, 0]

# create the path
path = np.array([[10, 10], [10, 60], [80, 80], [50, 10]])

robot_traj = rtb.mstraj(path[1:, :], qdmax=speed, q0=path[0, :], dt=0.1, tacc=tacc).q
total_time = robot_traj.shape[0] * dt + look_ahead / speed
print(robot_traj.shape)

sim = bdsim.BDSim(animation=True)
bd = sim.blockdiagram()


def background_graphics(ax):
    ax.plot(path[:, 0], path[:, 1], "r", linewidth=3, alpha=0.7)


def pure_pursuit(cp, R=None, traj=None):
    # find closest point on the path to current point
    d = np.linalg.norm(traj - cp, axis=1)  # rely on implicit expansion
    i = np.argmin(d)

    # find all points on the path at least R away
    (k,) = np.where(d[i + 1 :] >= R)  # find all points beyond horizon
    if len(k) == 0:
        # no such points, we must be near the end, goal is the end
        pstar = traj[-1, :]
    else:
        # many such points, take the first one
        k = k[0]  # first point beyond look ahead distance
        pstar = traj[k + i, :]
    return pstar.flatten()


speed = bd.CONSTANT(speed, name="speed")
pos_error = bd.SUM("+-", name="err")
# d2goal = bd.FUNCTION(lambda d: math.sqrt(d[0]**2 + d[1]**2), name='d2goal')
h2goal = bd.FUNCTION(lambda d: math.atan2(d[1], d[0]), name="h2goal")
heading_error = bd.SUM("+-", mode="c", name="herr")
Kh = bd.GAIN(0.5, name="Kh")
bike = bd.BICYCLE(x0=x0)
vplot = bd.VEHICLEPLOT(
    scale=[0, 80, 0, 80], size=0.7, shape="box", init=background_graphics
)  # , movie='rvc4_8.mp4')
sscope = bd.SCOPE(name="steer angle")
hscope = bd.SCOPE(name="heading angle")
stop = bd.STOP(lambda x: np.linalg.norm(x - np.r_[50, 10]) < 0.1, name="close_enough")
pp = bd.FUNCTION(
    pure_pursuit, fkwargs={"R": look_ahead, "traj": robot_traj}, name="pure_pursuit"
)

xy = bd.INDEX([0, 1], name="xy")
theta = bd.INDEX([2], name="theta")

bd.connect(pp, pos_error[0])
bd.connect(pos_error, h2goal)
# bd.connect(d2goal, stop)

bd.connect(h2goal, heading_error[0])
bd.connect(theta, heading_error[1], hscope)
bd.connect(heading_error, Kh)
bd.connect(Kh, bike.gamma, sscope)
bd.connect(speed, bike.v)

bd.connect(xy, pp, stop, pos_error[1])

bd.connect(bike, xy, theta, vplot)

bd.compile()

if __name__ == "__main__":
    sim.report(bd)
    out = sim.run(bd, T=total_time)
