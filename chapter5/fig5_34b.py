#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

car = Bicycle('steermax', 0.5)
randinit
rrt = RRT(car, 'npoints', 1000)

rrt.plan[]
##
rrt.plot[]
view(25, 35)

##
g = rrt.graph
clf
hold on
view[2]
axis([rrt.xrange rrt.yrange -10 5])
xlabel('x') ylabel('y'); zlabel('\theta')
grid on
view(25, 35)

#axis equal

#rrt.graph.plot('noedges', 'nocomponentcolor', 'NodeSize', 3, 'NodeFaceColor', 'b', 'NodeEdgeColor', 'b', 'edges')

for i=1:g.n
    c = g.coord(i)
    plot3(c[0], c[1], c[2], 'LineStyle' , 'none', 'Marker', 'o', 'MarkerSize', 6, 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'none')
    if i > 1
        p = g.vdata(i)
        pth = p.path
        k = find(g.neighbours(i) < i)
        pth = [pth g.coord(k)]
        plot3(pth(1,:), pth(2,:), pth(3,:), 'r')
    end
    
    pause(0.05)
end

hold off
rotate3d
            


