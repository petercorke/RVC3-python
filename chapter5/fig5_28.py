#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

lp = Lattice[]

## lattice after 1 iter
lp.plan('iterations', 1)
lp.plot[]
xaxis(-1,3) yaxis(-3,3)

rvcprint.rvcprint(subfig='a', 'nocmyk', 'thicken', 1.5)

## lattice after 2 iter
lp.plan('iterations', 2)
lp.plot[]
xaxis(-1,3) yaxis(-3,3)

rvcprint.rvcprint(subfig='b', 'thicken', 1.5)


## lattice after 7 iter
lp.plan('iterations', 8)
lp.plot[]
xaxis(-1,3) yaxis(-3,3)

rvcprint.rvcprint(subfig='c', 'thicken', 1.5)



