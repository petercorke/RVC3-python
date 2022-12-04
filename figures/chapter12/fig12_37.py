#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv

images = ImageCollection('campus/*.png', grey=True)

bag = BagOfWords(images, 2_000, seed=0)

w, f = bag.wordfreq()
print(len(w))

plt.bar(w, -np.sort(-f), width=1)
plt.xlim(0, bag.k)
plt.ylim(1, f.max())
plt.yscale('log')
plt.grid(True)
plt.xlabel('Visual word')
plt.ylabel('Number of occurences')

rvcprint.rvcprint()
