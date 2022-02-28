#!/usr/bin/env python3

# run with command line -a switch to show animation

import bdsim
import math
import numpy as np

sim = bdsim.BDSim()
bd = sim.blockdiagram()
from spatialmath import base

#x0 = [8, 5, math.pi/2]
x0 = [5, 2, 0]
L = [1, -2, 4]


def background_graphics(ax):
    base.plot_homline(L, "r--", ax=ax, xlim=np.r_[0, 10], ylim=np.r_[0, 10])
    ax.plot(x0[0], x0[1], 'o')

speed = bd.CONSTANT(0.5)
slope = bd.CONSTANT(math.atan2(L[0], -L[1]))
d2line = bd.FUNCTION(lambda u: (u[0] * L[0] + u[1] * L[1] + L[2])/math.sqrt(L[0]**2 + L[1]**2))
heading_error = bd.SUM('+-', mode='c')
steer_sum = bd.SUM('++')
Kd = bd.GAIN(0.5, name='Kd')
Kh = bd.GAIN(1, name='Kh')
bike = bd.BICYCLE(x0=x0, name='vehicle')
vplot = bd.VEHICLEPLOT(scale=[0, 10], size=0.7, shape='box', init=background_graphics)
hscope = bd.SCOPE(name='heading')

xy = bd.INDEX([0, 1], name='xy')
theta = bd.INDEX([2], name='theta')

bd.connect(d2line, Kd)
bd.connect(Kd, steer_sum[1])
bd.connect(steer_sum, bike.gamma)
bd.connect(speed, bike.v)

bd.connect(slope, heading_error[0])
bd.connect(theta, heading_error[1])

bd.connect(heading_error, Kh)
bd.connect(Kh, steer_sum[0])

bd.connect(xy, d2line)

bd.connect(bike, xy, theta, vplot)
bd.connect(theta, hscope)

bd.compile()

if __name__ == "__main__":
    bd.report()
    out = sim.run(bd, T=20)
