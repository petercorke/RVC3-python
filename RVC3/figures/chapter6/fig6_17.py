#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *

pg = PoseGraph('data/killian-small.toro')

pg.plot(text=False)
rvcprint.rvcprint(subfig='a')

pg.optimize()

plt.clf()
pg.plot(text=False)

rvcprint.rvcprint(subfig='b')

