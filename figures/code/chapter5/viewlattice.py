#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

function viewlattice(g, markeropt, lineopt, path)
    
    if isempty(markeropt)
        markeropt = {'bo', 'MarkerSize', 4, 'MarkerFaceColor', 'b'}
    end
    if isempty(lineopt)
        lineopt = {'Linewidth', 0.2, 'Color', [0.5 0.5 0.5]}
    end
    
    p = g.coord[]
    clf
    th = p(3,:)
    th(th == 3) = -1
    plot3(p(1,:), p(2,:), th*pi/2, markeropt{:})
    xlabel('x') ylabel('y'); zlabel('\theta')
    grid on
    hold on
    plot3(0, 0, 0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 8)
    view[-1,89]
    axis equal
    
    # draw the lattice
    for e=1:g.ne
        v = g.vertices(e)  # get the vertices of the edge
        
        drawarc(g, v[0], v[1], lineopt)
    end
    
    if nargin > 3
    
        # highlight the path
        for k=1:length(path)-1
            v1 = path(k)
            v2 = path(k+1)
            e1 = g.edges(v1) e2 = g.edges(v2)
            i = intersect(e1, e2)
            if length(i) > 1
                error('should be only one entry')
            end
            drawarc(g, v1, v2, {'Linewidth', 3, 'Color', 'k'})
        end
    end
end

function drawarc(g, v1, v2, lineOpts)
    Narc = 20
    
    p1 = g.coord(v1)
    p2 = g.coord(v2)
    
    # frame {N} is start of the arc
    theta = p1[2]*pi/2  # {0} -> {N}
    T_0N = SE2(p1(1:2), theta)
    
    dest = round( T_0N.inv * p2(1:2) )  # in {N}
    
    if dest[1] == 0
        # no heading change, straight line segment
            th = [p1[2] p2[2]]
    th(th == 3) = -1
        plot3([p1[0] p2[0]], [p1[1] p2[1]], th*pi/2, lineOpts{:})
    else
        # curved segment
        c = T_0N * [0 dest[1]]'


        th = ( linspace(-dest[1], 0, Narc) + p1[2] )*pi/2
        
        x = math.cos(th) + c[0]
        y = math.sin(th) + c[1]
        
        th0 = p1[2]
                th0(th0==3) = -1
                thf = p2[2]
        thf(thf==3) = -1
        plot3(x, y, linspace(th0, thf, Narc)*pi/2, lineOpts{:})
    end
end
