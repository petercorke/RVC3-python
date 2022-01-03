#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm

castle = Image.Read('castle.png', grey=True)

edges = castle.canny()
edges.disp(colormap='invert')
plt.xlim(400, 700)
plt.ylim(600, 300)
plt.grid(True)
rvcprint.rvcprint(debug=False, subfig='a')


Iu, Iv = castle.to('float32').gradients(Kernel.DGauss(2))
Iu.disp()
m = (Iu ** 2 + Iv ** 2).sqrt()
m.disp(colormap='invert')
plt.xlim(400, 700)
plt.ylim(600, 300)
plt.grid(True)

rvcprint.rvcprint(subfig='b')




