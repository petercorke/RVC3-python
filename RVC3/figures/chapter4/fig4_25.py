#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
import bdsim

import runpy

# TODO refactor this
dict = runpy.run_path("models/quadrotor.py")
g = globals()
for key in ['bd', 'sim']:
    g[key] = dict[key]

out = sim.run(bd, T=1.5, dt=0.05)
sim.options.animation = False
sim.options.graphics = True

rvcprint.rvcprint(interval=(1, 1, 2))
