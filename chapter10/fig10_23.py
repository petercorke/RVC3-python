import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

im = Image('parks.png')
im.disp(axes=False, title=False)
rvcprint.rvcprint(subfig='a')

im = Image('parks.png', gamma='sRGB', dtype='double')
im.disp(block=True)
gs = shadow_invariant(im.image, 0.7)
Image(gs).disp(interpolation='none', badcolor='red')

rvcprint.rvcprint(subfig='b')
