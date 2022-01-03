#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

im = Image.Read('parks.png')
im.disp(axes=False, title=False)
rvcprint.rvcprint(subfig='a')

im = Image.Read('parks.png', gamma='sRGB', dtype='float')
gs = shadow_invariant(im.image, 0.7)
Image(gs).disp(interpolation='none', badcolor='red')

rvcprint.rvcprint(subfig='b')
