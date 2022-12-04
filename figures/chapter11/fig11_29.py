#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *


objects = Image.Read('segmentation.png')
objects.disp(title=False)
rvcprint.rvcprint(subfig='a')

S = Kernel.Circle(3)
closed = objects.close(S)
closed.disp()
rvcprint.rvcprint(subfig='b')


clean = closed.open(S)
clean.disp()
rvcprint.rvcprint(subfig='c')

opened = objects.open(S)
clean = opened.close(S)
clean.disp()
rvcprint.rvcprint(subfig='d')


