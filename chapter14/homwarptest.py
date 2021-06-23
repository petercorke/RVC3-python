#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

im = iread('monalisa.png')

# image is 1m in front of camera: 0x + 0y + 1z - 1 = 0
cam = CentralCamera('image', im, 'distance', 1, ...
    'focal', 10e-3)
K = cam.K

n = [0 0 1] d = -2


T12 = SE3(0,0,-1)*SE3.Rx(-0)

T21 = (T12)
HE = T21.R + T21.t/d*n
H = K*HE*inv(K)

P = [1 1 -d]'

p1 = cam.project(P)
p2 = cam.project(P, 'Tcam', T12)

homtrans(H, p1)

#homwarp(H, im)

