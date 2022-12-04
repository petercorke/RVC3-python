#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

np.set_printoptions(linewidth=200)

images = ImageCollection('campus/*.png', mono=True)

features = []
for image in images:
    features += image.SIFT()

# image 2, (150,248), feature 88

# sort them in descending order by strength
features.sort(by="scale", inplace=True)
features[:10].table()

ex = []
for i in range(400):
    ex.append(features[i].support(images))


feature = features[108]
print(feature)

images[feature.id].disp()
feature.plot(filled=True, color='y', hand=True, alpha=0.5)

rvcprint.rvcprint(subfig='a')

feature.support(images).disp()
rvcprint.rvcprint(subfig='b')


# sf = isurf(images, 'thresh', 0)
# sf{1}
# sf = [sf{:}]
# sf[258]
# idisp(images(:,:,1), 'nogui')
# sf[258].plot('g+')
# sf[258].plot_scale('g', 'clock')
# rvcprint.rvcprint(subfig='a', 'svg')

# clf
# z = sf[258].support(images)
# idisp(z, 'nogui')




# z = Image.Zeros(500, 500)
# z = z.paste(Image.Constant(10, 10, 200), (100,200))
# z.disp()
# sf = z.SIFT()
# sf.table()

# sf.plot(filled=True, color='y', alpha=0.2)

# sf[0].support(z).disp()


# plt.show(block=True)


