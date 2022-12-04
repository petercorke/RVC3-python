#!/usr/bin/env python3
    
import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm

##
# lena = iread('lena.pgm')
# idisp(lena, 'nogui')
# rvcprint('svg', 'subfig', 'a')
# 
# eyes = iroi(lena, [239   359 237 294])
# idisp(eyes, 'nogui')
# rvcprint('svg', 'subfig', 'b')

##
mona = Image.Read('monalisa.png')

#smile = iroi(mona, [265 342 264 286])

mona.disp(grid=True)
rvcprint.rvcprint(subfig='a')

# eyes = mona.roi([239, 376, 170, 210])


smile = mona.roi([265, 342, 264, 286])
smile.disp(grid=True)
rvcprint.rvcprint(subfig='b')

