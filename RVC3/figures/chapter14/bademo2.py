#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# left=iread('left.jpg', 'reduce', 2)
# right=iread('right.jpg', 'reduce', 2)
# sl = isurf(left)
# sr = isurf(right)
# m=sl.match(sr)
# [F,r]=m.ransac(@fmatrix, 1e-4)

cam = CentralCamera('focal', 4.5e-3, 'pixel', 2*1.5e-6, 'resolution', [1224 1632])
# iphone has 1.5um pixels, double for the image subsampling


ba = BundleAdjust(cam)

c1 = ba.add_camera( SE3, 'fixed' )
c2 = ba.add_camera( T )

for j=1:length(m2)
    landmark = ba.add_landmark( P(:,j) )
    ba.add_projection(c1, landmark, m2(j).p1)
    ba.add_projection(c2, landmark, m2(j).p2)
end

ba

X = ba.getstate[]
# 
# #X=X+randn(size(X))*0.02
ee = ba.errors(X)

# XX = ba.optimize(X)
