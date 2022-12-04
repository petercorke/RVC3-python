#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from scipy.io import loadmat

# process Kinect images for book
data = loadmat('fig14_42.mat')

## IR image
ir = Image(data['ir'])
print(ir)
ir.disp(grid=True)
rvcprint.rvcprint(subfig='a')


## color image

rgb = Image(data['rgb'])
print(rgb)
rgb.disp(grid=True)

rvcprint.rvcprint(subfig='b')


## depth map
im = data['depth']

depth = Image(im)
print(depth)
depth.disp(grid=True, badcolor='red', colormap='viridis', colorbar=dict(shrink=0.8, aspect=20*0.8,label='Depth (m)'))
rvcprint.rvcprint(subfig='c')

# plt.show(block=True)



