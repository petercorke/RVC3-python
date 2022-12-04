#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import spatialmath.base as smb

images = ImageCollection('campus/*.png', mono=True)

bag = BagOfWords(images, 2_000, nstopwords=50, seed=0)
print(bag)

print(bag._labels[108]) # new label for feature 108

v10 = bag.wwfv(10)

sim = bag.similarity(v10)
rank = np.argsort(-sim)

# rank, sim = bag.closest(S, 10)

subfigs = 'abcd'

for k, i in enumerate(rank[:4]):
    images[i].disp(title=False)
    smb.plot_text((6, 6), f"image #{i}, similarity {sim[rank[k]]:.2f}", color='w', backgroundcolor='k', verticalalignment='top', fontsize=12)
    rvcprint.rvcprint(subfig=subfigs[k])
