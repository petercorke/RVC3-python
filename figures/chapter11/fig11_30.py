#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *


objects = Image.Read('segmentation.png')
S = Kernel.Circle(3)
closed = objects.close(S)
clean = closed.open(S)

eroded = clean.erode(S)

edge = clean - eroded
edge.disp()

rvcprint.rvcprint()
