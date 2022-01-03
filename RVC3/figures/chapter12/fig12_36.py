#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


images = ImageCollection('campus/*.png', mono=True)
bag = BagOfWords(images, 2_000, seed=0)
print(bag)


# tiles = []
# for i in range(400):
#     f = bag.features(i * 4 + 1)
#     tiles.append(f[0].support(images))
# zz = Image.Tile(tiles, 20).disp(plain=True)

# def showex(row, col):
#     w = (row * 20 + col) * 4 + 1
#     z = bag.exemplars(w)
#     z.disp(plain=True, title=f"#{w}")

w = bag.word(108)
print(w)
print(bag.occurrence(w))
print(bag.contains(w))


exemplars = bag.exemplars(w, bgcolor=255, columns=12, max=24)
exemplars.disp(plain=True)


rvcprint.rvcprint()
