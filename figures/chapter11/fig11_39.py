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

# Read YAML file
with open(mvtb_path_to_datafile("data/left_intrinsics.yml"), 'r') as f:
    calibration = yaml.safe_load(f)

dist_coeffs = np.array(calibration['distortion_coefficients']['data'])
C = np.reshape(calibration['camera_matrix']['data'], (3, 3))
print(C)

# get image 'left12.jpg'
distorted = images[11]
distorted.disp(title=False)
rvcprint.rvcprint(subfig='a')

undistorted = distorted.undistort(C, dist_coeffs)


distorted = images = Image.Read("calibration/left12.jpg")
import yaml
with open(mvtb_path_to_datafile("data/left_intrinsics.yml"), "r") as f:
    calibration = yaml.safe_load(f)

distort_coeffs = np.array(calibration["distortion_coefficients"]["data"])
k = distort_coeffs[[0, 1, 4]]; p = distort_coeffs[[2, 3]]
C = np.reshape(calibration["camera_matrix"]["data"], (3, 3))
u0, v0 = C[:2, 2]
fpix_u = C[0, 0]
fpix_v = C[1, 1]

Up, Vp = distorted.meshgrid()
u = (Up - u0) / fpix_u;
v = (Vp - v0) / fpix_v;

r = np.sqrt( u**2 + v**2 );
delta_u = u * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*u*v + p[1]*(r**2 + 2*u**2)
delta_v = v * (k[0]*r**2 + k[1]*r**4 + k[2]*r**6) + p[0]*(r**2 + 2*v**2) + p[1]*u*v

ud = u + delta_u; vd = v + delta_v;

U = ud * fpix_u + u0;
V = vd * fpix_v + v0;
cv.remap(distorted.A, U.astype("float32"), V.astype("float32"), cv.INTER_LINEAR)

undistorted.disp()

rvcprint.rvcprint(subfig='b')

# [Ui,Vi] = imeshgrid(distorted)
# Up = Ui Vp = Vi
# idisp(distorted, 'nogui')
# rvcprint('subfig', 'a', 'svg')

# load bouget
# k = kc([1 2 5]) p = kc([3 4])
# u0 = cc[0] v0 = cc[1]; fpix_u = fc[0]; fpix_v = fc[1]
# u = (Up-u0) / fpix_u
# v = (Vp-v0) / fpix_v
# r = sqrt( u.^2 + v.^2 )
# delta_u = u .* (k[0]*r.^2 + k[1]*r.^4 + k[2]*r.^6) + ...
#    2*p[0]*u.*v + p[1]*(r.^2 + 2*u.^2)
# delta_v = v .* (k[0]*r.^2 + k[1]*r.^4 + k[2]*r.^6) + ...
#    p[0]*(r.^2 + 2*v.^2) + 2*p[0]*u.*v
# ud = u + delta_u  vd = v + delta_v
# U = ud * fpix_u + u0
# V = vd * fpix_v + v0
# undistorted = interp2(Ui, Vi, distorted, U, V)
# idisp(undistorted, 'nogui')
# rvcprint('subfig', 'b', 'svg')

