#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


im = Image.Read('notre-dame.png')
print(im)
p1 =   np.array([
    [44.1364,  377.0654], 
    [94.0065,  152.7850],
    [537.8506,  163.4019],
    [611.8247,  366.4486]
]).T

mn = p1.min(axis=1)
mx = p1.max(axis=1)
p2 = np.array([
    [mn[0], mn[0], mx[0], mx[0]],
    [mx[1], mn[1], mn[1], mx[1]]
])

H, _ = CentralCamera.points2H(p1, p2, method='leastsquares')

warped = im.warp_perspective(H)
warped.disp(grid=True)

rvcprint.rvcprint()

md = im.metadata()
f = float(md['FocalLength'])
print(f)
cam = CentralCamera(imagesize=im.shape, f=f/1000, sensorsize=[7.18e-3, 5.32e-3])
print(cam)
sol, normal = cam.decomposeH(H)
print(sol.printline(orient="rpy/yxz"))
print(normal[0].T)
# tr2rpy(sol[1].T, 'deg', 'camera')
