#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

objects = Image.Read('segmentation.png')
S = Kernel.Circle(3)
closed = objects.close(S)
clean = closed.open(S)


skeleton = clean.thin()

bg = 1.0 - 0.2 * clean.to('float32') - 0.3 * skeleton.to('float32')
bg.disp()
rvcprint.rvcprint(subfig='a')

ends = skeleton.endpoint()

bg = bg.colorize()
comp = bg.switch(ends, [0, 0, 0])
comp.disp(grid=True)
plt.xlim(203, 326)
plt.ylim(358, 261)
rvcprint.rvcprint(subfig='b')

joins = skeleton.triplepoint()
comp = comp.switch(joins, [1, 1, 1])
comp.disp(grid=True)
plt.xlim(203, 326)
plt.ylim(358, 261)
rvcprint.rvcprint(subfig='c')


# skeleton = clean.thin()
# composite = clean * 0.3 + skeleton

# composite.disp(colormap='invert', grid=True)
# rvcprint.rvcprint(subfig='a')

# ends = skeleton.endpoint()
# ends.disp()
# composite = ends * 100 + clean * 0.3 + skeleton * 0.2
# composite.disp(colormap='invert', grid=True)
# plt.xlim(203, 326)
# plt.ylim(358, 261)
# rvcprint.rvcprint(subfig='b')

# joins = skeleton.triplepoint()
# joins.disp()
# composite = joins + clean * 0.3 + skeleton * 0.2
# composite.disp(colormap='invert', grid=True)
# plt.xlim(203, 326)
# plt.ylim(358, 261)
# rvcprint.rvcprint(subfig='c', debug=True)


# composite.disp(colormap='invert', grid=True)
# rvcprint.rvcprint(subfig='a')

# bg = (Image(255 * np.ones(objects.shape)) - clean * 0.3 - skeleton * 0.2).colorize()

# ends = skeleton.endpoint()
# composite = ends.colorize([255, 0, 0]) + bg