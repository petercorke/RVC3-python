#! /usr/bin/env python3
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3, base
import cv2 as cv

images = FileCollection('calibration/*.jpg')

K, distortion, frames = CentralCamera.images2C(images, gridsize=(7,6), gridpitch=0.025)

print(K)
print(distortion)
print(len(frames))

frames[4].frame.disp()
rvcprint.rvcprint(subfig='a')

cam = CentralCamera()

ax = base.plotvol3([-0.1, 0.3, -0.1, 0.3, -0.4, 0])
for id, frame in enumerate(frames):
    cam.plot_camera(pose=frame.T, scale=0.05, shape='camera')
    ax.text(*frame.T.t, f" {id}", zorder=20, fontsize=12)
shape = np.r_[7 * 0.025, 6 * 0.025, 0.01]
base.plot_cuboid(shape, centre=shape/2)

corner = np.r_[images[0].width, images[0].height] / K[0,0]
r = np.linalg.norm(corner) 
k1, k2, k3 = distortion[[0, 1, 4]]
duv = corner * (k1 * r**2 + k2 * r**4 + k3 * r**6)
print(duv)

rvcprint.rvcprint(subfig='b', interval=0.1)

