#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm

mona = Image.Read('monalisa.png', grey=True, dtype='float')
pyramid = mona.pyramid()
print(pyramid)

width = sum([im.width for im in pyramid])

out = Image.Constant(width, pyramid[0].height, 0.99)
u = 0
for im in pyramid:
    out.paste(im, [u, 0])
    u += im.width

out.disp()
rvcprint.rvcprint()
