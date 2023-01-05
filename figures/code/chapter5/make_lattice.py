#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

function g = make_lattice(niter, costs)

# function latticeplanner
    g = PGraph(3, 'distance', 'SE2') #@(x,y) norm(x(1:2) - y(1:2)) )

root = g.add_node( [0 0 0] )

destinations = [
    1  1  1
    0  1 -1
    0  1  3
    ]

if nargin < 2
    costs = [1 1 1]
end
# for i=1:numcols(destinations)
#     g.add_node( destinations(:,i), root, costs(i))
# end
    

for iteration=1:niter
    # find all current leaf nodes
    nodes = find(g.connectivity_out == 0)
    #nodes = 1:g.n
    for node=nodes # foreach node
        
        # get the pose of this node
        pose = g.coord(node)
        xys = pose(1:2) heading = pose[2]
        

        
        # transform the motion directions to this pose and b
        xy = bsxfun(@plus, xys, homtrans(rotm2d(heading*pi/2), destinations(1:2,:)))
        theta = mod(heading+destinations(3,:), 4)
        newDestinations = [xy theta]
        
        # now add paths to these new poses
        for i=1:numcols(destinations)
            # check to see if the pose already exists
# #             [v,d] = g.closest(newDestinations(:,i))
# #             if d < 0.5
                        v = g.closest(newDestinations(:,i), 0.5)
                        if ~isempty(v)
                # node already exists, check existing neighbours

                    # no such edge exists, add it
                    g.add_edge(node, v, costs(i))
 

            else
                # node doesn't exist, add it and an edge
                nv = g.add_node( newDestinations(:,i), node, costs(i))

            end
        end

    end
end

fprintf('#d nodes created\n', g.n)
# clf
# g.plot('labels')
# xyzlabel
# axis equal

# xaxis(-.25, 3.5) yaxis(-3.5, 3.5)
# grid on

# A-star search
# dest = g.closest([6 8 0]')
# [path,cost] = g.Astar(1, dest)
# g.highlight_path(path)
# g.coord(path)

