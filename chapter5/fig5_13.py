#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

load house
ds = Dstar(house)
tic
profile on
ds.plan(place.kitchen)
profile off
toc
ds.niter
p = ds.query(place.br3, 'animate')
ds.plot(p)

rvcprint.rvcprint('opengl')
