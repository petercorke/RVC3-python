import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from spatialmath import SE3
from matplotlib import cm
import spatialmath.base as smb

# set background to grey
im = Image(np.zeros((50, 40)), dtype='uint8')

# create the four objects
im = im.paste(np.ones((10,10)), [10,10])  # big square
im = im.paste(np.ones((5,5)), [12,25])  # small square

# add the protrusions to big square
im = im.paste(np.ones((1,2)), [8,15])
im = im.paste(np.ones((2,1)), [15,8])

# join the 2 squares
im = im.paste(np.ones((6,1)), [14, 20])


im = im.paste(np.ones((2,20)), [5,40])  # horizontal line
im = im.paste(np.ones((20,2)),[35,5])  # vertical line

# put hole in big square
im = im.paste(np.zeros((2,2)), [14, 14])


im = Image(im.image.T)
im.write('eg-morph2.png')
im.disp(block=True)

