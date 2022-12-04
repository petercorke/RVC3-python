#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt


import runpy

# TODO refactor this
dict = runpy.run_path("models/braitenberg.py")
g = globals()
for key in ['bd', 'sim']:
    g[key] = dict[key]

# Simulate the model
sim.set_options(animation = False, graphics = True, hold=False)
out = sim.run(bd, T=125, dt=0.2)

# make fig 1 current
plt.figure(1)
plt.title('')  # remove the title
plt.plot(out.x[:,0], out.x[:,1], color='w', label='vehicle path')
plt.legend(loc='lower right')

rvcprint.rvcprint()


