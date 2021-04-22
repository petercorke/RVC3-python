import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

flowers = Image('flowers4.png')

options = dict(title=False, axes=False
)
flowers.disp(**options)
rvcprint.rvcprint(subfig='a', format='png')

hsv = flowers.colorspace('hsv')

hsv.plane(2).disp(**options)  # H
rvcprint.rvcprint(subfig='b', format='png')

hsv.plane(1).disp(**options)  # S
rvcprint.rvcprint(subfig='c', format='png')

hsv.plane(0).disp(**options)  # V
rvcprint.rvcprint(subfig='d', format='png')


lab = flowers.colorspace('lab')

lab.plane(1).disp(**options)  # A*
rvcprint.rvcprint(subfig='e', format='png')

lab.plane(0).disp(**options)  # B*
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
