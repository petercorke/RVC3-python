#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv

cv.setRNGSeed(0)

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

tiles = Image.Tile(ex, columns=20).colorize()
tiles.draw_circle((442, 286), 50, color=[255, 255, 0], thickness=5)
tiles = tiles.disp(plain=True)
rvcprint.rvcprint()


