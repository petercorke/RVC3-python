#!/usr/bin/env python3

import bdsim
import math
import numpy as np
from spatialmath import SE2

sim = bdsim.BDSim(animation=True)
bd = sim.blockdiagram()

def sensorfield(x, y):
    xc = 60
    yc = 90;
    return 200 / ((x - xc) ** 2 + (y - yc) ** 2 + 200)

def background_graphics(ax):
    v = np.arange(0, 100)
    X, Y = np.meshgrid(v, v)
    Z = sensorfield(X, Y)
    a = ax.imshow(Z, cmap='viridis')
    ax.figure.colorbar(a)
    
speed = bd.CONSTANT(2, name='speed')
sum1 = bd.SUM('+--')
sum2 = bd.SUM('+-')

Kv = bd.GAIN(5, name='Kv')
Ks = bd.GAIN(5, name='Ks')
bike = bd.BICYCLE(x0=[5, 5, 0], name='vehicle')
pose = bd.MUX(nin=3, name='pose')

def sensorfunc(x, offset):
    xy = SE2(x) * offset
    return sensorfield(xy[0], xy[1])[0]

# offset = np.r_[0, 2]
leftsensor = bd.FUNCTION(sensorfunc, nin=1, args=([0, -2],), name='leftsensor')
rightsensor = bd.FUNCTION(sensorfunc, nin=1, args=([0, 2],), name='rightsensor')

vplot = bd.VEHICLEPLOT(scale=[0, 100], size=2, shape='box', init=background_graphics)
vscope = bd.SCOPE(name='velocity')
wscope = bd.SCOPE(name='steering rate')

bd.connect(bike[0:3], pose[0:3], vplot[0:3])
bd.connect(pose, leftsensor, rightsensor)
bd.connect(rightsensor, sum1[1], sum2[0])
bd.connect(speed, sum1[0])
bd.connect(leftsensor, sum1[2], sum2[1])
bd.connect(sum1, Kv)
bd.connect(Kv, vscope, bike.v)

bd.connect(sum2, wscope, Ks)
bd.connect(Ks, bike.gamma)

bd.compile()

if __name__ == "__main__":
    bd.report()

    out = sim.run(bd, T=100, dt=0.2)

    sim.done(bd, block=True)
