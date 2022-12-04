#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm



castle = Image.Read('castle.png', grey=True, dtype='float')

Du = Kernel.Sobel()
Iu = castle.convolve(Du)
Iv = castle.convolve(Du.T)

Iu.disp(colormap='signed')
rvcprint.rvcprint(subfig='a')

Iv.disp(colormap='signed')
rvcprint.rvcprint(subfig='b')

Iu = castle.convolve(Kernel.DGauss(sigma=2));
Iv = castle.convolve(Kernel.DGauss(sigma=2).T);

m = (Iu ** 2 + Iv ** 2).sqrt()
m.disp(black=0.4)
rvcprint.rvcprint(subfig='c')

plt.clf()
# th = np.arctan2(Iv.image, Iu.image)
th = Iu.direction(Iv)
s = 10
plt.quiver(np.arange(0, castle.width, 20), np.arange(0, castle.height, 20), 
       Iu.image[::20, ::20], Iv.image[::20, ::20], scale=s)
plt.xlim(0, castle.width)
plt.ylim(0, castle.height)
plt.xlabel('u (pixels)')
plt.ylabel('v (pixels)')
rvcprint.rvcprint(subfig='d')
