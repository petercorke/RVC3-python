#!/usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib import cm
import spatialmath.base as smb

images = FileCollection("mosaic/aerial2-*.png", grey=True)

# initialize the canvas for pasting in the frames
composite = Image.Zeros(size=(2_500, 2_500))
composite = composite.paste(images[0], (0, 0))
composite.disp(block=False)

frames = []

for image in images[1:]:
    f1 = composite.SIFT()

    fi = image.SIFT()
    m = f1.match(fi)

    H, _ = m.estimate(CentralCamera.points2H, "ransac", confidence=0.99)

    tile, topleft, corners = image.warp_perspective(H, inverse=True, tile=True)
    frames.append(corners)
    composite = composite.paste(tile, topleft, "blend")

    # show the mosaic so far
    composite.disp(reuse=True, grid=True, block=False)
    print(f"adding frame {image.name}")
    smb.plot_polygon(corners, "r", close=True)  # add the outlines
    plt.pause(1)

print("all added")
plt.show(block=True)
