#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)


L.anaglyph(R, 'rc').disp()

rvcprint.rvcprint(subfig='b')