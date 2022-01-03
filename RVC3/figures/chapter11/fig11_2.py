#!/usr/bin/env python3
import matplotlib
import rvcprint
from machinevisiontoolbox.base import iread, idisp

flowers, name = iread('flowers8.png')
print(flowers[276, 318, :])

# idisp(flowers, block=True)

flowers.disp()
rvcprint.rvcprint()
