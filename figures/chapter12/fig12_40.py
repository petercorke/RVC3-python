#!/usr/bin/env python3

#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import cv2 as cv
import spatialmath.base as smb

images = ImageCollection('campus/*.png', grey=True)

bag = BagOfWords(images, 2_000, seed=0)
print(bag)

testimages = ImageCollection('campus/holdout/*.png', grey=True)

# S = bag.similarity(testimages)
# print(np.argmax(S, axis=1))

subfigs = "abcd"

for i in range(2):
    testimages[i].disp()
    smb.plot_text((6, 6), f"query image #{i}", color='w', backgroundcolor='k', verticalalignment='top', fontsize=12)
    rvcprint.rvcprint(subfig=subfigs[2*i])

    k, s = bag.retrieve(testimages[i])

    images[k].disp()
    smb.plot_text((6, 6), f"retrieved image #{k}, similarity {s:.2f}", color='w', backgroundcolor='k', verticalalignment='top', fontsize=12)
    rvcprint.rvcprint(subfig=subfigs[2*i+1])
