#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3, base
import cv2 as cv

images = ImageCollection('calibration/*.jpg', rgb=False)
print(images)

K, distortion, frames = CentralCamera.images2C(images, gridshape=(7,6), squaresize=0.025)

print(K)
print(distortion)
print(len(frames))

F = [2, 4, 6, 8]
subfigs = "abcd"
for i in range(4):
    frames[F[i]].image.disp()
    print(images.names[i])
    rvcprint.rvcprint(subfig=subfigs[i])