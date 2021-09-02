#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## Visual odometry example
#   - stereo camera
#   - ICP between frames

# run fig 57 first

tz2 = tz
tz2(ebundle>20) = NaN
subplot[210] plot(tz2, '.-', 'MarkerSize', 15)
yaxis(0,1.5)
xaxis(2,length(tz))
ylabel('camera displacement (m)')
grid
subplot[211] plot(ebundle, '.-', 'MarkerSize', 15)
set(gca, 'YScale', 'log')
xaxis(2,length(tz))
hold on
plot([2,length(tz)], [20 20], 'r--')
xlabel('Time step')
ylabel('total error (pix^2)')
grid

rvcprint.rvcprint[]

median(tz(ebundle<20))

