#! /usr/bin/env python3
import rvcprint
from math import pi
from spatialmath.base import *
import matplotlib.pyplot as plt

plotvol2([-0.2, 5, -0.2, 5], grid=True)

T0 = transl2(0, 0)
trplot2(T0, frame='0', color='k')

TA = transl2(1, 2) @ trot2(30, 'deg')

trplot2(TA, frame='A', color= 'b')
TB = transl2(2, 1)
trplot2(TB, frame='B', color='r')
TAB = TA @ TB
trplot2(TAB, frame='AB', color='g')
TBA = TB @ TA
trplot2(TBA, frame='BA', color='c')
P = [3, 2]

plot_point(P, 'ko', text='P', color='k')

rvcprint.rvcprint()