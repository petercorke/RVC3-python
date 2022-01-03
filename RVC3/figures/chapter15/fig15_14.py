#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

camera = CentralCamera.Default(name='')

## line servoing

ibvs = IBVS_l.Example(camera)
ibvs.run(5)

rvcprint.rvcprint(ax=ibvs.ax_camera, facecolor=None)

