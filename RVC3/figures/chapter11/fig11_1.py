#!/usr/bin/env python3
import rvcprint
from machinevisiontoolbox.base import iread, idisp
# import matplotlib; matplotlib.use('TkAgg')

street, name = iread('street.png')

idisp(street)
rvcprint.rvcprint()
