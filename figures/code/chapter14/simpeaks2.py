#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

function simpeaks2(DSI, u, v)
    clf
    plot(squeeze(DSI(v,u,:)), '-o', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'b', 'MarkerSize', 6)
    yaxis([-1 1])
    grid
    xlabel('Disparity $d - d_{min}$ (pixels)', 'Interpreter', 'LaTeX')
    ylabel('NCC similarity')
    text(5, -0.9, sprintf('pixel at (#d,#d)', u, v), 'FontSize', 11)

