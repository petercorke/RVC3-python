#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3

ev = EarthView()


ev.grab(-27.475722, 153.0285, zoom=17).disp()
rvcprint.rvcprint(subfig='a')

ev.grab(-27.475722, 153.0285, zoom=17, type='roadmap').disp()
rvcprint.rvcprint(subfig='b')
