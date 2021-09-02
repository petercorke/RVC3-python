#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv
from BagOfWords import BagOfWords

images = FileCollection('campus/*.png', grey=True)

cv.setRNGSeed(0)
bag = BagOfWords(images, 2_000)

w, f = bag.wordfreq()

plt.bar(w, -np.sort(-f), width=1)
plt.xlim(0, bag.k)
plt.ylim(0, f.max())
plt.grid(True)
plt.xlabel('Visual word')
plt.ylabel('Number of occurences')

rvcprint.rvcprint()
