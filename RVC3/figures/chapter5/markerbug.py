#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

clf

hold on
#background
for i=1:1000
    plot3(rand[0,1], rand[0,1] ,rand[0,1], 'k.-', 'MarkerSize', 8)
end

# green line
x = linspace(0, 1, 200)
y = 0.5*ones(size(x))
z = 0*y
plot(x, y,  'go', 'MarkerSize', 10, 'MarkerFaceColor', 'g')

# black marker on top
plot(0.5, 0.5, 'kh', 'MarkerSize', 15, 'MarkerFaceColor', 'k')
