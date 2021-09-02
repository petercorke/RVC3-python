#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm

im = Image.Read('eg-morph1.png')
print(im)

S1 = np.ones((5, 5))
e1 = im.morph(S1, 'min')
d1 = e1.morph(S1, 'max')
# im.disp()
# e1.disp()
# d1.disp(block=True)

S2 = np.ones((7, 7))
e2 = im.morph(S2, 'min')
d2 = e2.morph(S2, 'max')

S3 = np.ones((1,13))
e3 = im.morph(S3, 'min')
d3 = e3.morph(S3, 'max')


# def tile(tiles, sep=0, sepcolor=0):

#     # TODO tile a sequence into specified shape

#     # work with different types
#     out = None

#     for row in tiles:
#         tilerow = None
#         for im in row:
#             if tilerow is None:
#                 tilerow = im.image
#             else:
#                 # add border to the left
#                 im = cv.copyMakeBorder(im.image, 0, 0, sep, 0, cv.BORDER_CONSTANT, value=sepcolor)
#                 tilerow = np.hstack((tilerow, im))
#         if out is None:
#             out = tilerow
#         else:
#             # add border to the top
#             tilerow = cv.copyMakeBorder(tilerow, sep, 0, 0, 0, cv.BORDER_CONSTANT, value=sepcolor)
#             out = np.vstack((out, tilerow))
#     if len(base.getvector(sepcolor)) == 3:
#         return Image(out, colororder='RGB')
#     else:
#         return Image(out)

# results = tile([[im, e1, d1], [im, e2, d2], [im, e3, d3]], sep=1, sepcolor=1)
# results.disp(title='bb')

results = Image.Tile([im, e1, d1, im, e2, d2, im, e3, d3], columns=3, sep=1, bgcolor=0)
results.disp()

SE = Image(np.zeros((results.shape[0], 25), dtype='uint8'))
SE = SE.paste(S1, [5,15])
SE = SE.paste(S2, [5,55])
SE = SE.paste(S3, [5,115])
SE.disp()
# plt.show(block=True)
results = results.colorize([255, 255, 255])
# results.disp(black=0.4, title='results')

SE = SE.colorize([255, 0, 0])

out = Image.Hstack([results, SE], sep=1, bgcolor=[255, 255, 255])
out.disp(black=0.4, axes=False)

rvcprint.rvcprint(debug=True)
