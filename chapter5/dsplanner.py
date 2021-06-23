#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

function dsplanner(ds)
    
    assert(isstruct(ds))
    assert(isa(ds.niter, 'uint32'))
    assert(isa(ds.verbose, 'logical'))
    assert(isa(ds.changed, 'logical'))
    
    assert(isa(ds.b, 'uint32')) # backpointer (0 means not set)
    assert(isa(ds.t, 'uint8')) # tag: NEW OPEN CLOSED
      assert(isa(ds.h, 'single')) # distance map, path cost
        # list of open states: 2xN matrix
        #   each open point is a column, row 1 = index of cell, row 2 = k
        assert(isa(ds.openlist, 'uint32'))
    assert(isa(ds.openlist_maxlen, 'uint32'))  # keep track of maximum length
        # tag state values
    assert(isa(ds.NEW), 'uint8')
        assert(isa(ds.OPEN), 'uint8') 
    assert(isa(ds.CLOSED), 'uint8') 



#             ds.b = zeros(size(ds.costmap), 'uint32')  # backpointers
#             ds.t = zeros(size(ds.costmap), 'uint8')   # tags
#             ds.h = Inf*ones(size(ds.costmap))         # path cost estimate
#             ds.openlist = zeros[1,-1]               # the open list, one column per point
# 
#             ds.openlist_maxlen = -Inf
            
    

    ds.niter = 0
    while true
        ds.niter = ds.niter + 1
        
        if PROCESS_STATE(ds) < 0
            break
        end
        if ds.verbose
            disp(' ')
        end
    end

    ds.changed = false
end


# The main D* function as per the Stentz paper, comments Ln are the original
# line numbers.
function r = PROCESS_STATE(d)
    
    ## states with the lowest k value are removed from the
    ## open list
    X = d.MIN_STATE[]                          # L1
    
    if isempty(X)                               # L2
        r = -1
        return
    end
    
    k_old = GET_KMIN(d) DELETE(d,X);          # L3
    
    if k_old < d.h(X)                           # L4
        for Y=neighbours(d,X)                   # L5
            if (d.h(Y) <= k_old) && (d.h(X) > d.h(Y)+d.c(Y,X))  # L6
                d.b(X) = Y
                d.h(X) = d.h (Y) + d.c(Y,X)                    # L7
            end
        end
    end
    
    ## can we lower the path cost of any neighbours?
    if k_old == d.h(X)                          # L8
        for Y=neighbours(d,X)                   # L9
            if (d.t(Y) == d.NEW) || ...                         # L10-12
                    ( (d.b(Y) == X) && (d.h(Y) ~= (d.h(X) + d.c(X,Y))) ) || ...
                    ( (d.b(Y) ~= X) && (d.h(Y) > (d.h(X) + d.c(X,Y))) )
                d.b(Y) = X INSERT(d,Y, d.h(X)+d.c(X,Y), 'L13');   # L13
            end
        end
    else                                        # L14
        for Y=neighbours(d,X)                   # L15
            if (d.t(Y) == d.NEW) || ( (d.b(Y) == X) && (d.h(Y) ~= (d.h(X) + d.c(X,Y))) )
                d.b(Y) = X INSERT(d,Y, d.h(X)+d.c(X,Y), 'L18');   # L18
            else
                if ( (d.b(Y) ~= X) && (d.h(Y) > (d.h(X) + d.c(X,Y))) )
                    INSERT(dX, d.h(X), 'L21')                    # L21
                else
                    if (d.b(Y) ~= X) && (d.h(X) > (d.h(Y) + d.c(Y,X))) && ...
                            (d.t(Y) == d.CLOSED) && d.h(Y) > k_old
                        INSERT(d,Y, d.h(Y), 'L25')                # L25
                    end
                end
            end
        end
    end
    
    r = 0
    return
end

function kk = k(ds, X)
    i = ds.openlist(1,:) == X
    kk = ds.openlist(2, i)
end

function INSERT(ds, X, h_new, where)
    
    i = find(ds.openlist(1,:) == X)
    if length(i) > 1
        error('D*:INSERT: state in open list #d times', X)
    end
    
    if ds.t(X) == ds.NEW
        k_new = h_new
        # add a new column to the open list
        ds.openlist = [ds.openlist [X k_new]]
    elseif ds.t(X) == ds.OPEN
        k_new = min( ds.openlist(2,i), h_new )
    elseif ds.t(X) == ds.CLOSED
        k_new = min( ds.h(X), h_new )
        # add a new column to the open list
        ds.openlist = [ds.openlist [X k_new]]
    end
    
    if numcols(ds.openlist) > ds.openlist_maxlen
        ds.openlist_maxlen = numcols(ds.openlist)
    end
    
    ds.h(X) = h_new
    ds.t(X) = ds.OPEN
end

function DELETE(ds, X)
    i = find(ds.openlist(1,:) == X)
    if length(i) ~= 1
        error('D*:DELETE: state #d doesnt exist', X)
    end
    ds.openlist(:,i) = [] # remove the column
    ds.t(X) = ds.CLOSED
end

# return the index of the open state with the smallest k value
function ms = MIN_STATE(ds)
    if isempty(ds.openlist)
        ms = []
    else
        # find the minimum k value on the openlist
        [~,i] = min(ds.openlist(2,:))
        
        # return its index
        ms = ds.openlist(1,i)
    end
end

function kmin = GET_KMIN(ds)
    kmin = min(ds.openlist(2,:))
end

# return the cost of moving from state X to state Y
function cost = c(ds, X, Y)
    [r,c] = ind2sub(size(ds.costmap), [X Y])
    dist = sqrt(sum(diff([r c]).^2))
    dcost = (ds.costmap(X) + ds.costmap(Y))/2
    
    cost = dist * dcost
end

# return index of neighbour states as a row vector
function Y = neighbours(ds, X)
    dims = size(ds.costmap)
    [r,c] = ind2sub(dims, X)
    
    # list of 8-way neighbours
    Y = [r-1 r-1 r-1 r r  r+1 r+1 r+1 c-1 c c+1 c-1 c+1 c-1 c c+1]
    k = (min(Y)>0) & (Y(1,:)<=dims[0]) & (Y(2,:)<=dims[1])
    Y = Y(:,k)
    Y = sub2ind(dims, Y(1,:)', Y(2,:)')'
end

