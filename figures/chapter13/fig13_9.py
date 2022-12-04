#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm
from spatialmath import Twist2
import yaml
import cv2 as cv

images = ImageCollection('calibration/left*.jpg')

# # Read YAML file
# with open(mvtb_path_to_datafile("data/left_intrinsics.yml"), 'r') as f:
#     calibration = yaml.safe_load(f)

# dist_coeffs = np.array(calibration['distortion_coefficients']['data'])
# C = np.reshape(calibration['camera_matrix']['data'], (3, 3))
# print(C)

K, distortion, frames = CentralCamera.images2C(images, gridshape=(7,6), squaresize=0.025)

# get image 'left12.jpg'
distorted = images[11]
distorted.disp(title=False)
rvcprint.rvcprint(subfig='a')
#----------------------------------------------------------------------- #

k = distortion[[0, 1, 4]]; p = distortion[[2, 3]]
u0, v0 = K[:2, 2]
fpix_u = K[0, 0]
fpix_v = K[1, 1]

Ud, Vd = distorted.meshgrid()
u = (Ud - u0) / fpix_u;
v = (Vd - v0) / fpix_v;

r = np.sqrt( u**2 + v**2 );
delta_u = u * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*u*v + p[1]*(r**2 + 2*u**2)
delta_v = v * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*(r**2 + 2*v**2) + p[1]*u*v

ud = u + delta_u; vd = v + delta_v;

U = ud * fpix_u + u0;
V = vd * fpix_v + v0;
undistorted = distorted.warp(U, V)

undistorted.disp()

rvcprint.rvcprint(subfig='b')



