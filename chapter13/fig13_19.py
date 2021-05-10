#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


square = Image.Squares(number=1, shape=256, color=128).rotate(0.3)
edges = square.canny()
edges.disp(black=0.3, grid=True, title=False)
rvcprint.rvcprint(subfig='a')

h = Hough(edges)

h.plot_accumulator()
print(h.nz, h.t)
cbar = plt.colorbar()
cbar.set_label('Votes')
rvcprint.rvcprint(subfig='b')
plt.xlim(1.2, 1.350)
plt.ylim(210, 240)
rvcprint.rvcprint(subfig='c')

plt.figure()
plt.plot(h.votes)
plt.yscale('log')
plt.xlim(0, h.t)
plt.ylim(1, h.votes[0])
plt.xlabel('Threshold')
plt.ylabel('Number of votes above threshold')
plt.grid(True)
rvcprint.rvcprint(subfig='d')


lines = h.lines(80)
# lines = lines[[0,2,5],:]
print(lines)
square.disp(black=0.3, grid=True)
h.plot_lines(lines)
rvcprint.rvcprint(subfig='e')

# plt.show(block=True)
