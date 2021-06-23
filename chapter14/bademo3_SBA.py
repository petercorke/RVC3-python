#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# load Lourakis SBA problem
#  cant make it converge

## setup the problem

clf

cam = CentralCamera('default')

# files containing initial motion & structure estimates and intrinsic parameters
camsfname='sba-1.6/demo/7cams.txt' #'/home/lourakis/cmp/bt.cams'
ptsfname='sba-1.6/demo/7pts.txt' #'/home/lourakis/cmp/bt.pts'
calfname='sba-1.6/demo/calib.txt' #'/home/lourakis/cmp/bt.cal'

# camsfname='sba-1.6/demo/9cams.txt' #'/home/lourakis/cmp/bt.cams'
# ptsfname='sba-1.6/demo/9pts.txt' #'/home/lourakis/cmp/bt.pts'
# calfname='sba-1.6/demo/calib.txt' #'/home/lourakis/cmp/bt.cal'

ba = BundleAdjust(cam)

ba.load_sba(camsfname, ptsfname, calfname)
ba

## solve it

X = ba.getstate[]
# 
# #X=X+randn(size(X))*0.02
ee = ba.errors(X)

XX = ba.optimize(X)


