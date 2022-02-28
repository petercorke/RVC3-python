#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt

# from machinevisiontoolbox import *
# from mayavi import mlab
# from mayavi.api import Engine
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, similarity, DSI = L.stereo_simple(R, 3, [40, 90])

print(DSI.shape)

fig, axes = plt.subplots(ncols=2, nrows=2, sharey=True, sharex=True)
# d = plt.subplot_mosaic('ABb;CDb')
for i, (ax, v) in enumerate(zip(axes.ravel(), np.arange(100, 541, 100))):
    mappable = ax.imshow(DSI[v, :, :].T)
    ax.set_xlim(0, DSI.shape[0])
    ax.set_ylim(0, 50)
    ax.set_aspect('auto')
    ax.text(420, 3, f"v={v}", backgroundcolor="white")
    if i > 1:
        ax.set_xlabel('u (pixels)')
    if i % 2 == 0:
        ax.set_ylabel('disparity (pixels)')

plt.subplots_adjust(bottom=0.1, right=0.80, top=0.9)
cax = plt.axes([0.83, 0.1, 0.03, 0.8])
plt.colorbar(mappable, cax=cax, label='ZNCC similarity')

rvcprint.rvcprint()

