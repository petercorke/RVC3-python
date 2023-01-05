#!/usr/bin/env python3
import matplotlib
from RVC3.tools import rvcprint
from machinevisiontoolbox.base import iread, idisp

flowers, name = iread('flowers8.png')

idisp(flowers)
rvcprint.rvcprint()
