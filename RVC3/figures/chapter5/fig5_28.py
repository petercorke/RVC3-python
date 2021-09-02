#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *


qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

dubins = DubinsPlanner(curvature=1)
dpath, dstatus = dubins.query(qs, qg)

segs = np.cumsum(dstatus.seglengths)
curvs = {'L': 1, 'S': 0, 'R': -1}
dcurv = []
for s in np.linspace(0, dstatus.length, 100):
    seg = np.sum(s > segs)
    curv = curvs[dstatus.segments[seg]]
    dcurv.append(curv)
dcurv = np.array(dcurv)

cpoly = CurvaturePolyPlanner()
cpath, cstatus = cpoly.query(qs, qg)

ccurv = []
poly = cstatus.poly
print(cstatus)

ccurv = np.polyval(poly, np.linspace(0, cstatus.length, 100))

s = np.linspace(0, 1, 100)
plt.step(s, dcurv, label='Dubins')
plt.plot(s, ccurv, label='CubicPoly')
plt.xlabel('normalized path distance $s$')
plt.ylabel('curvature $\kappa$')
plt.xlim(0, 1)
plt.legend()

rvcprint.rvcprint()