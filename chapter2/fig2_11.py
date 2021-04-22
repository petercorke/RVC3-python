import rvcprint
from math import pi
from spatialmath.base import *
import matplotlib.pyplot as plt

plotvol2([0, 5, 0, 5], grid=True)
T1 = transl2(1, 2) @ trot2(30, 'deg')

trplot2(T1, frame='1', color= 'b')
T2 = transl2(2, 1)
trplot2(T2, frame='2', color='r')
T3 = T1 @ T2
trplot2(T3, frame='3', color='g')
T4 = T2 @ T1
trplot2(T4, frame='4', color='c')
P = [3,  2 ]

plot_point(P, 'ko', text='P', textcolor='k', fillcolor='k')

rvcprint.rvcprint()