#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import spatialmath.base as smb

# load .enpeda dataset, 12bit pixel values
images = ZipArchive('bridge-l.zip', filter='*.pgm', grey=True, dtype='uint8', maxintval=4095, roi=[20, 750, 20, 480])
ax = plt.gca()
for image in images:
    ax.clear()
    image.disp(ax=ax)
    smb.plot_text((20, 420), f"frame {image.id}", color='w', backgroundcolor='k', fontsize=12)
    features = image.ORB(nfeatures=200)
    
    features.plot()
    plt.pause(0.02)

    if image.id > 15:
        break

rvcprint.rvcprint()
