#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

flowers = Image.Read('flowers4.png')

options = dict(title=False, axes=False
)
flowers.disp(**options)
rvcprint.rvcprint(subfig='a', format='png')

hsv = flowers.colorspace('HSV')

hsv.plane('H').disp(**options)  # H
rvcprint.rvcprint(subfig='b', format='png')

hsv.plane('S').disp(**options)  # S
rvcprint.rvcprint(subfig='c', format='png')

hsv.plane('V').disp(**options)  # V
rvcprint.rvcprint(subfig='d', format='png')


lab = flowers.colorspace('L*a*b*')

lab.plane('a*').disp(**options)  # A*
rvcprint.rvcprint(subfig='e', format='png')

lab.plane('b*').disp(**options)  # B*
rvcprint.rvcprint(subfig='f', format='png')


# idisp(hsv(:,:,1), 'plain')
# rvcprint.rvcprint(subfig='b', 'format', 'png')

# idisp(hsv(:,:,2), 'plain')
# rvcprint.rvcprint(subfig='c', 'format', 'png')

# lab = colorspace('RGB->Lab', flowers)

# idisp(lab(:,:,1), 'plain')
# rvcprint.rvcprint(subfig='d', 'format', 'png')

# idisp(lab(:,:,2), 'plain')
# rvcprint.rvcprint(subfig='e', 'format', 'png')

# idisp(lab(:,:,3), 'plain')
# rvcprint.rvcprint(subfig='f', 'format', 'png')
