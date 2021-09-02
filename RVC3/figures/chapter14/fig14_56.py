#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import spatialmath.base as smb

# load .enpeda dataset, 12bit pixel values
images = ZipArchive('bridge-l.zip', grey=True, dtype='uint8', maxintval=4095, roi=[20, 750, 20, 480])
for image in images:
    plt.clf()
    plt.imshow(image.A, cmap='gray')
    smb.plot_text((20, 420), f"frame {image.id}", color='w', backgroundcolor='k', fontsize=12)
    features = image.ORB(nfeatures=200)
    
    features = features.plot('k+')
    plt.pause(0.02)

    if image.id > 15:
        break

rvcprint.rvcprint
