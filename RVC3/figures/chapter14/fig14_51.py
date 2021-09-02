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


# tiles = []
# for i in range(400):
#     f = bag.features(i * 4 + 1)
#     tiles.append(f[0].support(images))
# zz = Image.Tile(tiles, 20).disp(plain=True)

# def showex(row, col):
#     w = (row * 20 + col) * 4 + 1
#     z = bag.exemplars(w)
#     z.disp(plain=True, title=f"#{w}")

exemplars = bag.exemplars(379, bgcolor=255, columns=12, max=24)
exemplars.disp(plain=True)


rvcprint.rvcprint()
