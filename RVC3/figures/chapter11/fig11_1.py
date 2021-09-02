#!/usr/bin/env python3
import rvcprint
from machinevisiontoolbox.base import iread, idisp

street, name = iread('street.png')
street.dtype
street[199,299]

streetd = street.astype('float')
street.dtype

street_d = iread('street.png', dtype='float')

idisp(street)

rvcprint.rvcprint()

# EPS gives weird button colors
