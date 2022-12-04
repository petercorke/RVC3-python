#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


mona = Image.Read('monalisa.png', grey=True, dtype='float')
G, L, s = mona.scalespace(8, 8)
Image.Tile(G, columns=8).disp(width=500)
rvcprint.rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

Image.Tile(L, columns=8).disp(width=500, colormap='signed')
rvcprint.rvcprint(subfig='b')
