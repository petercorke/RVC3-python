#! /usr/bin/env python

"""
Creates Fig 9.13
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import site
import numpy as np
import bdsim

site.addsitedir("bdsim")

from vloop import vloop

sim = bdsim.BDSim()
ploop = sim.blockdiagram()

Kp = 4000.0
Kff = 0.0
G = 107.815

# define blocks
inp = ploop.INPORT(3, onames=("theta*", "w*", "tau_d"), name="in")
outp = ploop.OUTPORT(4, name="out")  # inames=('theta', 'theta_err'),
sum1 = ploop.SUM("+-")
sum2 = ploop.SUM("++")
kp = ploop.GAIN(Kp, name="Kp")
kff = ploop.GAIN(Kff, name="Kff")
gearbox = ploop.GAIN(1 / G)
theta = ploop.INTEGRATOR(x0=0)
fftorque = ploop.CONSTANT(0)
VLOOP = ploop.SUBSYSTEM(vloop, name="VLOOP")

# s1 = ploop.SCOPE()
# s2 = ploop.SCOPE()
# s3 = ploop.SCOPE()

# wire them up
ploop.connect(inp[0], sum1[0])
ploop.connect(theta, sum1[1])
ploop.connect(sum1, kp, outp[1])  # theta_err
ploop.connect(kp, sum2[0])
ploop.connect(inp[1], kff)
ploop.connect(kff, sum2[1])
ploop.connect(sum2, VLOOP[0])
ploop.connect(inp[2], VLOOP[1])
ploop.connect(fftorque, VLOOP[2])
ploop.connect(VLOOP[0], gearbox)
ploop.connect(gearbox, theta)  # theta
ploop.connect(theta, outp[0])

ploop.connect(VLOOP[1], outp[2])
ploop.connect(VLOOP[2], outp[3])


# if __name__ == "__main__":
#     # test harness
#     bd = bdsim.BlockDiagram()

#     # position = bd.LSPB(0) HACK
#     position = bd.STEP(T=0.5, on=1, name='tghack')
#     vel = bd.CONSTANT(0)
#     taud = bd.CONSTANT(20 / G)
#     # speed = bd.WAVEFORM(wave='triangle', freq=2, amplitude=25)
#     PLOOP = bd.SUBSYSTEM(ploop, name='PLOOP')
#     scope = bd.SCOPE(nin=2, name=r'$\omega$', labels=['actual', 'demand'])

#     bd.connect(position, PLOOP[0], scope[0])
#     bd.connect(vel, PLOOP[1])
#     bd.connect(taud, PLOOP[2])
#     bd.connect(PLOOP[0], scope[1])

#     bd.compile()   # check the diagram
#     bd.report()    # list all blocks and wires

#     out = bd.run(1, dt=1e-3)
#     bd.done(block=True)
