#!/usr/bin/env python3

# now dilate


import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *


im = Image.Read('eg-morph2.png')
print(im)

S1 = np.ones((5, 5))
e1 = im.morph(S1, 'max')
d1 = e1.morph(S1, 'min')
# im.disp()
# e1.disp()
# d1.disp(block=True)

S2 = np.ones((7, 7))
e2 = im.morph(S2, 'max')
d2 = e2.morph(S2, 'min')

S3 = np.ones((1,13))
e3 = im.morph(S3, 'max')
d3 = e3.morph(S3, 'min')




results = tile([[im, e1, d1], [im, e2, d2], [im, e3, d3]], sep=1, sepcolor=1)
# results.disp(title='bb')


SE = Image(np.zeros((results.shape[0], 25)))
SE = SE.paste(S1, [5,15])
SE = SE.paste(S2, [5,55])
SE = SE.paste(S3, [5,115])
# SE.disp()

results = results.colorize([255, 255, 255])
# results.disp(black=0.4, title='results')

SE = SE.colorize([255, 0, 0])

out = tile([[results, SE]], sep=1, sepcolor=[255, 255, 255])
out.disp(black=0.4, axes=False)

rvcprint.rvcprint()
