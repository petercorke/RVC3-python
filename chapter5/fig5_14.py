#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

load house

ds.modify_cost( [300,325115,125], 5 )


tic
ds.plan('noprogress') # replan
toc
ds.niter
p = ds.query(place.br3)
ds.plot(p)

hold on
plot_box([300 325 115 125], 'y:', 'LineWidth', 2)

rvcprint.rvcprint('opengl')
