#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

clf
hold on
for vel = [-1 1]*0.5
    for gamma = [-1:0.2:1]
        p = pathsim([0 0 0], [vel gamma])
        if vel > 0
            color = 'b'
        else
            color = 'r'
        end
        plot2(p, color)
        
        plot2([p(:,1:2) -4*ones(numrows(p),1)], 'Color', 0.8*[1 1 1])
        
    end
end
grid
xlabel('x') ylabel('y'); zlabel('\theta')
view[33,47]

rvcprint.rvcprint
