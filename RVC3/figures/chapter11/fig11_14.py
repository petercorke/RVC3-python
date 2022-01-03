#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *


mona = Image.Read('monalisa.png', grey=True, dtype='float')
mona.disp(title=False)
rvcprint.rvcprint(subfig='a')


K = np.ones((21, 21)) / 21 ** 2
mona.convolve(K).disp()
rvcprint.rvcprint(subfig='b')


K = Kernel.Gauss(5)
mona.convolve(K).disp()
rvcprint.rvcprint(subfig='c')

