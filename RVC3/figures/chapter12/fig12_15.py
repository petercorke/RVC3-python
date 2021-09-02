#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

sharks = Image.Read('sharks.png')

fv = sharks.blobs()

print(np.array(fv[1].contour()).shape)

polar = fv[1].polar()
s = np.linspace(0, 1, polar.shape[1])

fig, ax1 = plt.subplots()
color = 'blue'
ax1.plot(s, polar[0, :] / polar[0, :].max(), color=color)
ax1.set_ylabel('normalized radius', color=color)
ax1.tick_params(axis='y', labelcolor=color)
plt.grid(True)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'red'
ax2.plot(s, polar[1, :], color=color)
ax2.set_ylabel('angle (radians)', color=color)
ax2.tick_params(axis='y', labelcolor=color)

ax1.set_xlim(0, 1)
ax1.set_xlabel('normalized perimeter distance')

rvcprint.rvcprint(subfig='a')

plt.clf()
for i in range(4):
    polar = fv[i].polar()
    if i == 3:
        plt.plot(s, polar[0, :] / polar[0, :].max(), '--')
    else:
        plt.plot(s, polar[0, :] / polar[0, :].max())

plt.ylabel('normalized radius')
plt.xlim(0, 1)
plt.xlabel('normalized perimeter distance')
plt.grid(True)


rvcprint.rvcprint(subfig='b')

print(fv.polarmatch(1))