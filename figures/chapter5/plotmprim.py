#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

clf
markeropt = {'bo', 'MarkerSize', 4, 'MarkerFaceColor', 'b'}

        lineopt = {'Linewidth', 0.2, 'Color', [0.5 0.5 0.5]}
        
    xlabel('x') ylabel('y')
    grid on
    hold on
    #axis equal
    
for i=1:numel(local)
    ep = local(i).endpose_c
    if ep[1] >= 0
                plot(local(i).poses(end,1), local(i).poses(end,2), markeropt{:})

    plot(local(i).poses(:,1), local(i).poses(:,2), lineopt{:})
    end
end
    plot(0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8)

