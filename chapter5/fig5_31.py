#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

load road
lp = Lattice(road, 'grid', 5, 'root', [50 50 0], 'cost', [1 1 1])
lp.plan
lp.plot
lp.query([30 45 0], [50 20 0])
lp.plot[]

rvcprint.rvcprint
