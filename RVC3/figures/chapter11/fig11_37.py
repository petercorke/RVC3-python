#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm
from spatialmath import Twist2

mona = Image.Read('monalisa.png', grey=True, dtype='float')

Up, Vp = Image.meshgrid(width=500, height=500)

U = 4 * (Up - 100)
V = 4 * (Vp - 200)

mona.warp(U, V).disp()
rvcprint.rvcprint(subfig='a')

M = np.array([[0.5, 0, 100], [0, 0.5, 200]])

out = mona.affine_warp(M, bgcolor=np.nan)
out.disp(badcolor='r')

rvcprint.rvcprint(subfig='b')

tw = Twist2.UnitRevolute([300, 300])
M = tw.exp(np.pi / 6).A[:2, :]

out = mona.affine_warp(M, bgcolor=np.nan)
out.disp(badcolor='r')

rvcprint.rvcprint(subfig='c')

