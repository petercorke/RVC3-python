#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm
from spatialmath import Twist2
import yaml

# Read YAML file
with open("left_intrinsics.yml", 'r') as stream:
    calibration = yaml.safe_load(stream)

dist_coeffs = np.array(calibration['distortion_coefficients']['data'])
C = np.reshape(calibration['camera_matrix']['data'], (3, 3))
print(C)

distorted = Image.Read('left12.jpg')
distorted.disp(title=False)
rvcprint.rvcprint(subfig='a')

undistorted = distorted.undistort(C, dist_coeffs)
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

