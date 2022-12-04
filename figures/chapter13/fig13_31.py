#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from math import pi
from spatialmath import SE3
import math


scene = Image.Read('lab-scene.png', rgb=False)
print(scene)
scene.disp()

# a = scene.image
# print(a.__array_interface__)

# b = scene.image[:, :, ::-1]  # BGR order
# print(b.__array_interface__)

# print(np.shares_memory(a,b))
# idisp(b)

# plt.show(block=True)
cam = CentralCamera(f=4.25e-3, imagesize=(4032, 3024), pp=(2016, 1512), rho=1.4e-6)
print(cam)
print(cam.K)


markers = scene.fiducial("4x4_50", K=cam.K, side=67e-3)
for marker in markers:
    print(marker)
    marker.draw(scene, length=0.10, thick=20)

scene.disp()

rvcprint.rvcprint()
