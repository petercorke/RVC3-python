# fig 9.7

from math import pi
import numpy as np
from roboticstoolbox.models.DH import Puma560

import bdsim

vloop = bdsim.BlockDiagram(name='vloop')

Kv = 0.6
Ki = 0
Km = 0.228
J = 580e-6
B = 817e-6
tau_lim = 0.9
G = 107.815

# define the block connections
inp = vloop.INPORT(3)
out = vloop.OUTPORT(4)

# define the blocks
integrator = vloop.INTEGRATOR(x0=0)
sum1 = vloop.SUM('+-')
sum2 = vloop.SUM('++')
sum3 = vloop.SUM('++')
sum4 = vloop.SUM('-+')
kv = vloop.GAIN(Kv, name='Kv')
ki = vloop.GAIN(Ki, name='Ki')
km = vloop.GAIN(Km, name='Km')
kff = vloop.GAIN(1 / Km, name='Kff')
limiter = vloop.CLIP(min=-tau_lim, max=tau_lim, name='torquelimit')
motor = vloop.LTI_SISO(1, [J, B], name='motor')

# connect the blocks
vloop.connect(inp[0], sum1[0])
vloop.connect(motor, sum1[1], out[0])
vloop.connect(sum1, out[1], kv, integrator)
vloop.connect(integrator, ki)
vloop.connect(kv, sum2[0])
vloop.connect(ki, sum2[1], out[3])
vloop.connect(sum2, sum3[0])
vloop.connect(inp[2], kff)
vloop.connect(kff, sum3[1])
vloop.connect(sum3, km)
vloop.connect(km, limiter)
vloop.connect(limiter, sum4[1], out[2])
vloop.connect(inp[1], sum4[0])
vloop.connect(sum4, motor)

bd = bdsim.BlockDiagram()

disturbance = bd.CONSTANT(0)
feedforward = bd.CONSTANT(0)
# speed = bd.WAVEFORM(wave='triangle', freq=2, amplitude=25)
speed = bd.INTERPOLATE(x=(0, 0.1, 0.3, 0.4, 0.6, 1), y=(0, 0, 50, 50, 0, 0), time=True, name='demand')
subsystem = bd.SUBSYSTEM(vloop)
xy = bd.SCOPE(nin=2, name=r'$\omega$', labels=['actual', 'demand'])

bd.connect(disturbance, subsystem[2])
bd.connect(speed, subsystem[0], xy[1])
bd.connect(feedforward, subsystem[1])
bd.connect(subsystem[0], xy[0])

n1 = bd.SCOPE(name=r'$\omega_{err}$')
n2 = bd.SCOPE(name=r'$\tau$')
n3 = bd.SCOPE(name='integral')
bd.connect(subsystem[1], n1)
bd.connect(subsystem[2], n2)
bd.connect(subsystem[3], n3)

bd.compile()   # check the diagram
bd.report()    # list all blocks and wires

out = bd.run(1, dt=1e-3)
# out = vloop.run(2, checkstep=1e-6)  # simulate for 5s
# # vloop.dotfile('bd1.dot')  # output a graphviz dot file
# # vloop.savefig('pdf')      # save all figures as pdf
bd.done(block=True)

disturbance.value = -20 / G
out = bd.run(1, dt=1e-3)
# out = vloop.run(2, checkstep=1e-6)  # simulate for 5s
# # vloop.dotfile('bd1.dot')  # output a graphviz dot file
# # vloop.savefig('pdf')      # save all figures as pdf
bd.done(block=True)