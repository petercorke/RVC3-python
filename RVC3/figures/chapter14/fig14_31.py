#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, sim, DSI = L.stereo_simple(R, 3, [40, 90])

# print(np.nanmax(sim.image), np.nanmin(sim.image))


sim.disp(badcolor='red', colorbar=dict(shrink=0.92, aspect=20*0.92, label='ZNCCC similarity peak'))

rvcprint.rvcprint(subfig='a')

# # Image(np.isnan(sim.image)).disp()

# # there are no infs if window w/2=3, a few when window w/2=1
# plt.clf()
# im = sim.colorize()

# im = im.switch(np.isinf(sim.image), 'red')
# im = im.switch(np.isnan(sim.image), 'red')
sim.choose('blue', sim<0.6).disp()
rvcprint.rvcprint(subfig='b')
