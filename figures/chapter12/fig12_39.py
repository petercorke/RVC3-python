#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv

images = ImageCollection('campus/*.png', mono=True)
holdout = ImageCollection('campus/holdout/*.png', mono=True)


cv.setRNGSeed(0)
bag = BagOfWords(images, 2_000, nstopwords=50)

S = bag.similarity(holdout)

plt.figure()
plt.imshow(S)

plt.xlabel('Bag image index')
plt.ylabel('Query image index')

plt.xticks(np.arange(0, S.shape[1], 2))
plt.yticks(np.arange(0, S.shape[0], 2))
# plt.gca().set_aspect(0.8)
plt.colorbar(label='Similarity', shrink=0.25, aspect=20*0.25)

rvcprint.rvcprint()
