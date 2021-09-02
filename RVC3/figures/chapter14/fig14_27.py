#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)

disparity, sim, DSI = L.DSI(R, 3, [40, 90])

print(np.isinf(DSI.flatten()).sum())

print(np.nanmax(sim.image), np.nanmin(sim.image))
sim.disp(badcolor='red', colorbar=dict(label='ZNCCC similarity peak'))

rvcprint.rvcprint(subfig='a')

# Image(np.isnan(sim.image)).disp()

# there are no infs if window w/2=3, a few when window w/2=1
plt.clf()
im = sim.colorize()

im = im.switch(np.isinf(sim.image), 'red')
im = im.switch(np.isnan(sim.image), 'red')
im = im.switch(sim<0.6, 'blue')

im.disp()
rvcprint.rvcprint(subfig='b')
