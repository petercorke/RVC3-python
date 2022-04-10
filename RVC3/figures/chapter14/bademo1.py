#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm



# minimalistic problem, 4 cameras, 20 points

cam = CentralCamera('default')


ba = BundleAdjust(cam)

T = SE3(0.2, 0, 0)  # horizontal shift

c1 = ba.add_camera( SE3) #, 'fixed')
# c2 = ba.add_camera( T )
# c3 = ba.add_camera( T*T )
# c4 = ba.add_camera( T*T*T )
c2 = ba.add_camera( SE3 )
c3 = ba.add_camera( SE3 )
c4 = ba.add_camera( SE3 )

randinit
P = bsxfun(@plus, 2 * 2*(rand(3, 20) - 0.5), [-1, 0 , 6]')

for j=1:numcols(P)
    landmark = ba.add_landmark( P(:,j) )
    [p, visible] = cam.project(P(:,j))
    if visible
        ba.add_projection(c1, landmark, p)
    end
    [p, visible] = cam.project(P(:,j), 'Tcam', T)
    if visible
        ba.add_projection(c2, landmark, p)
    end
    [p, visible] = cam.project(P(:,j), 'Tcam', T*T)
    if visible
        ba.add_projection(c3, landmark, p)
    end
    [p, visible] = cam.project(P(:,j), 'Tcam', T*T*T)
    if visible
        ba.add_projection(c4, landmark, p)
    end 
end

ba


X = ba.getstate[]
ba.errors(X)
# 
# #X=X+randn(size(X))*0.02
#X[6] = 0.3
X(7:24) = X(7:24) + randn(1,3*6)*0.05
ee = ba.errors(X)

XX = ba.optimize(X)
