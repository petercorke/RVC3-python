#!/usr/bin/env python3

# Based on code by Pascal Getreuer 2006
# Demo for colorspace.m - the CIE xyY "tongue"
# Based on xycolorspace.m

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from machinevisiontoolbox.base.color import _normalize

nm = 1e-9

# define the spectrum
λ = np.arange(380.0, 750.0, 0.5) * nm

# convert to xyz chromaticity coords
xyz = ccxyz(λ)
x = xyz[:, 0]
y = xyz[:, 1]

# Convert from xyY to XYZ
Y = luminos(λ) / 683

X = Y * x / y
Z = Y * (1-x-y) / y

XYZ = np.array((X, Y, Z), dtype=np.float32).T.reshape(1, -1, 3)
RGB = colorspace_convert(XYZ, 'xyz', 'rgb')
RGB = _normalize(RGB)
RGB = gamma_encode(RGB)

im = Image(RGB, colororder='RGB')

# Convert from XYZ to R'G'B'
# im = imxyz.colorspace('xyz2bgr')
im.disp(extent=(380, 750, 0, 60))

plt.xlabel('Wavelength (nm)')
plt.ylabel('')
plt.gca().get_yaxis().set_visible(False)
plt.grid(color='w', linestyle='--')


rvcprint.rvcprint()

