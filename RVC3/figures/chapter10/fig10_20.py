#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.patches import Polygon

wedge = np.linspace(0, 1, 11).reshape(1,-1)

im = Image(wedge)
im.disp(extent=(-0.05, 1.05, 0, 0.2))
plt.ylabel('')
plt.gca().get_yaxis().set_visible(False)

rvcprint.rvcprint(interval=0.1)

