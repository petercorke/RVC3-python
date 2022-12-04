#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
from matplotlib.colors import ListedColormap

import pickle
disparity, similarity, DSI = pickle.load(open('DSI.p', 'rb'))

disparity_refined, A = Image.DSI_refine(DSI)

A.disp(colorbar=dict(shrink=0.92, aspect=20*0.92))
rvcprint.rvcprint(subfig='a')
#----------------------------------------------------------------------- #

disparity_refined.disp(colorbar=dict(shrink=0.92, aspect=20*0.92))

rvcprint.rvcprint(subfig='b')

