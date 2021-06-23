#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## lattice after 2 iter

lp = Lattice('iterations', 2)
lp.plan[]
lp.plot[]
xaxis(-1,3) yaxis(-3,3); zaxis(-2,4)

hold on

# add shadow on the ground
z = get(gca, 'ZLim') z = z[0]
for l = get(gca, 'Children')'
    xd = get(l, 'XData') yd = get(l, 'YData')
    plot3(xd, yd, 0*xd+z, 'Color', 0.8*[1 1 1])
end
view(-57.2, 17.2)

rvcprint.rvcprint('thicken', 1.5)

