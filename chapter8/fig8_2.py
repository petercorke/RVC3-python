import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath import *
import matplotlib.pyplot as plt
import numpy as np

puma = models.DH.Puma560()
# puma.name = ''

options = {
    'robot': {'alpha': 0.5},
    'shadow': {'alpha': 0.7},
    'jointaxes': {'color': 'black'},
    'jointlabels': {'size': 11},
}
puma.plot(puma.qn, jointlabels=True, name=False, backend='pyplot', options=options)

rvcprint.rvcprint(thicken=None)