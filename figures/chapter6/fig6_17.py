#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox.mobile import *

pg = PoseGraph('data/pg1.g2o')
print(pg.graph)
pg.optimize(animate=True, retain=True,
    eopt=dict(linewidth=0.5), vopt=dict(markersize=4), text=False)

# pg.graph.plot(colorcomponents=False, edge=dict(linewidth=2, color='black'), text=dict(fontsize=12))
pg.plot(eopt=dict(color='none'), vopt=dict(color='none'), text=dict(fontsize=12))
plt.xlabel('x')
plt.ylabel('y')

rvcprint.rvcprint()
