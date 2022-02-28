#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from spatialmath.base import plot_box


square = Image.Squares(number=1, size=256, fg=128).rotate(0.3)
edges = square.canny()
edges.disp(black=0.1, grid=True, title=False)
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

h = edges.Hough()

h.plot_accumulator(cmap='viridis_r')
print(h.nz, h.t)
cbar = plt.colorbar()
cbar.set_label('Votes')

plot_box(lrbt=(1.2, 1.350, 210, 240), color='k')
rvcprint.rvcprint(subfig='b')

# ----------------------------------------------------------------------- #

plt.xlim(1.2, 1.350)
plt.ylim(210, 240)
rvcprint.rvcprint(subfig='c')

# ----------------------------------------------------------------------- #

plt.figure()
plt.plot(h.votes, label='number of votes')
plt.yscale('log')
plt.xlim(0, h.t)
plt.ylim(1, h.votes[0])
plt.xlabel('Threshold')
plt.ylabel('Number of votes above threshold')
plt.gca().axvline(60, color='r', linestyle='--', label='threshold')
plt.legend()
plt.grid(True)
rvcprint.rvcprint(subfig='d')

# ----------------------------------------------------------------------- #

lines = h.lines(60)
# lines = lines[[0,2,5],:]
print(lines)
square.disp(black=0.1, grid=True)
h.plot_lines(lines)
rvcprint.rvcprint(subfig='e')

# plt.show(block=True)
