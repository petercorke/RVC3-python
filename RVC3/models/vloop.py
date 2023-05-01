#! /usr/bin/env python

"""
Creates Fig 9.7
Robotics, Vision & Control for Python, P. Corke, Springer 2023.
Copyright (c) 2021- Peter Corke
"""

import numpy as np
import bdsim

sim = bdsim.BDSim()
vloop = sim.blockdiagram()

Kv = 0.6
Ki = 0
Km = 0.228
J = 580e-6
B = 817e-6
tau_lim = 0.9
G = 107.815

# define the block connections
inp = vloop.INPORT(3, name="in")
out = vloop.OUTPORT(4, name="out")

# define the blocks
integrator = vloop.INTEGRATOR(x0=0)
sum1 = vloop.SUM("+-")
sum2 = vloop.SUM("++")
sum3 = vloop.SUM("++")
sum4 = vloop.SUM("-+")
kv = vloop.GAIN(Kv, name="Kv")
ki = vloop.GAIN(Ki, name="Ki")
km = vloop.GAIN(Km, name="Km")
kff = vloop.GAIN(1 / Km, name="Kff")
limiter = vloop.CLIP(min=-tau_lim, max=tau_lim, name="torquelimit")
motor = vloop.LTI_SISO(1, [J, B], name="motor")

# connect the blocks
vloop.connect(inp[0], sum1[0])  # omega*
vloop.connect(motor, sum1[1], out[0])
vloop.connect(sum1, out[1], kv, integrator)
vloop.connect(integrator, ki)
vloop.connect(kv, sum2[0])
vloop.connect(ki, sum2[1], out[3])
vloop.connect(sum2, sum3[0])
vloop.connect(inp[2], kff)  # feedforward
vloop.connect(kff, sum3[1])
vloop.connect(sum3, km)
vloop.connect(km, limiter)
vloop.connect(limiter, sum4[1], out[2])
vloop.connect(inp[1], sum4[0])  # tau_d
vloop.connect(sum4, motor)
