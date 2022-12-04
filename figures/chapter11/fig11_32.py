#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath.base import plot_circle

objects = Image.Read('segmentation.png')
S = Kernel.Circle(3)
closed = objects.close(S)
clean = closed.open(S)


skeleton = clean.thin()

bg = clean.to('float32') - 0.2 * skeleton.to('float32')
bg.disp()
rvcprint.rvcprint(subfig='a')

ends = skeleton.endpoint()


comp = bg.choose((0.5), ends)
comp.disp(grid=True)
plot_circle(5, ends.nonzero(), color="r")
plt.xlim(203, 326)
plt.ylim(358, 261)
rvcprint.rvcprint(subfig='b')

joins = skeleton.triplepoint()
comp = comp.choose(0, joins)
comp.disp(grid=True)
plot_circle(5, joins.nonzero(), color="r")
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