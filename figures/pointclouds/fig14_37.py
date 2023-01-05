#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
# from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# compute disparity
L = Image.Read('rocks2-l.png', reduce=1)
R = Image.Read('rocks2-r.png', reduce=1)
disparity = L.stereo_SGBM(R, 3, [2*40, 2*90], (2*200, 2))

# map to world coordinates
b = 0.160 # m
f = 3740  # pixels
di = disparity.image * 2 + 274
U, V = L.meshgrid()

u0 = L.width / 2
v0 = L.height / 2

X = b * (U - u0) / di
Y = b * (V - v0) / di
Z = f * b / di

cam = CentralCamera(f=f, imagesize=L.shape)
pcd = PointCloud(Z, image=L, camera=cam, depth_trunc=1.9)
pcd.transform(SE3.Rx(np.pi))

view = {
			"front" : [ 0.31299127017122574, 0.02154681571003491, 0.9495115583969268 ],
			"lookat" : [ 0.03055555680218866, 0.030925927187669552, -1.1837890148162842 ],
			"up" : [ -0.0343613671057671, 0.99934501124934461, -0.011350988576774189 ],
			"zoom" : 0.69999999999999996
		}


pcd.write("fig14_37.pcd")
