#!/usr/bin/env python3

import rvcprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from pgraph import *
import numpy as np
from roboticstoolbox.mobile import *


qs = (0, 0, np.pi/2)
qg = (1, 0, np.pi/2)

cpoly = CurvaturePolyPlanner()
path, status = cpoly.query(qs, qg)
print(status)
cpoly.plot(path)

rvcprint.rvcprint()