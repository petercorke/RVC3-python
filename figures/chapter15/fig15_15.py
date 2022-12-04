#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *


# visual servo with circle


ibvs = IBVS_e.Example(plotvol=[-1, 2, -1, 2, -1, 3.5])
ibvs.run(10)

ibvs.camera.clf()
ibvs.camera.plot_point(ibvs.history[0].p, 'ro', markerfacecolor='w')
ibvs.camera.plot_point(ibvs.history[-1].p, 'b*')
rvcprint.rvcprint(facecolor=None)