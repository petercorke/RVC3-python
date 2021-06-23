#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import cv2 as cv
import spatialmath.base as smb

images = FileCollection('campus/*.png', grey=True)

from BagOfWords import BagOfWords

cv.setRNGSeed(0)
bag = BagOfWords(images, 2_000)
print(bag)

S = bag.similarity(bag)

rank, sim = bag.closest(S, 10)

subfigs = 'abcd'

for k, i in enumerate(rank[:4]):
    images[i].disp(title=False)
    smb.plot_text((6, 6), f"image #{i}, similarity {sim[k]:.2f}", color='w', backgroundcolor='k', verticalalignment='top', fontSize=12)
    rvcprint.rvcprint(subfig=subfigs[k])
