#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv

images = FileCollection('campus/*.png', grey=True)


cv.setRNGSeed(0)
bag = BagOfWords(images, 2_000)

S = bag.similarity(images)

plt.figure()
plt.imshow(S)

plt.xlabel('Image index')
plt.ylabel('Image index')
plt.colorbar(label='Similarity')

rvcprint.rvcprint()
