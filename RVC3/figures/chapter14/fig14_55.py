#!/usr/bin/env python3

#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import cv2 as cv
import spatialmath.base as smb
from BagOfWords import BagOfWords

cv.setRNGSeed(0)

images = FileCollection('campus/*.png', grey=True)

bag = BagOfWords(images, 2_000)
print(bag)

testimages = FileCollection('campus/holdout/*.png', grey=True)
bag2 = bag.recall(testimages)
print(bag2)

S = bag.similarity(bag2)

bestmatch = S.argmax(axis=0)



for i in range(2):
    testimages[i].disp()
    smb.plot_text((6, 6), f"query image #{i}", color='w', backgroundcolor='k', verticalalignment='top', fontSize=12)
    rvcprint.rvcprint(subfig=subfigs[2*k])

    images[bestmatch[i]].disp()
    smb.plot_text((6, 6), f"recall image #{bestmatch[i]}, similarity {S[bestmatch[i], i]:.2f}", color='w', backgroundcolor='k', verticalalignment='top', fontSize=12)
    rvcprint.rvcprint(subfig=subfigs[2*k+1])
