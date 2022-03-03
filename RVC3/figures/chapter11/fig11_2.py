#!/usr/bin/env python3
import matplotlib
import rvcprint
from machinevisiontoolbox.base import iread, idisp

flowers, name = iread('flowers8.png')

idisp(flowers)
rvcprint.rvcprint()
