#!/usr/bin/env python3
from RVC3.tools import rvcprint
from machinevisiontoolbox.base import iread, idisp
# import matplotlib; matplotlib.use('TkAgg')

street, name = iread('street.png')

idisp(street)
rvcprint.rvcprint()
