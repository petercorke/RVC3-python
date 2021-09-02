#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from math import pi
from spatialmath import SE3
import math

scene = Image.Read('kitchen.jpg')
print(scene.EXIF())

cam = CentralCamera(f=4.25e-3, imagesize=(4032, 3024), pp=(2016, 1512), rho=1.4e-6)
print(cam)
print(cam.K)

im = scene.A

markers = scene.fiducial("5x5_50", K=cam.K, side=50e-3)
for marker in markers:
    print(marker)
    im = marker.draw(im, cam.K, length=0.07, thick=40)

Image(im).disp()

rvcprint.rvcprint()