#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

def simpeaks2(DSI, u, v):
    u = round(u)
    v = round(v)

    plt.plot(np.squeeze(DSI[v, u, :]), '-o', markerfacecolor='b', markeredgecolor='b', markersize=6)
    plt.xlim(0, DSI.shape[2])
    plt.ylim(-1, 1)
    plt.grid(True)
    plt.xlabel('Disparity $d - d_{min}$ (pixels)')
    plt.ylabel('NCC similarity')
    plt.text(5, -0.9, f"pixel at ({u}, {v})", fontsize=11)


L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, max, DSI = L.DSI(R, 3, [40, 90])

disparity.disp(grid=True, badcolor='red', colorbar=dict(label='Disparity (pixels)'))
max.disp(grid=True)
plt.show()

while True:
    print('waiting for click')
    plt.figure(1)
    uv = plt.ginput(1, timeout=0)
    if uv is None or len(uv) == 0:
        continue
    print(uv)
    plt.figure()
    try:
        simpeaks2(DSI, *uv[0])
    except:
        pass
    plt.pause(0.1)


