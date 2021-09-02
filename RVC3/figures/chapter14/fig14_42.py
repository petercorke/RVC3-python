#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm


(rtb) >>> import cv2 as cv

(rtb) >>> a=cv.ppf_match_3d_ICP(20)

(rtb) >>> a.registerModelToScene(data, model)
https://stackoverflow.com/questions/56809980/how-to-import-all-the-points-from-a-pcd-file-into-a-2d-python-array
http://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html?highlight=icp
load bunny
M = bunny
T_unknown = SE3(0.2, 0.2, 0.1) * SE3.rpy(0.2, 0.3, 0.4)
D = T_unknown * M

clf
plot2(M', 'r.', 'MarkerSize', 20)
hold on
plot2(D', 'b.', 'MarkerSize', 8)
hold off
xyzlabel
rvcprint.rvcprint(subfig='a')


corresp = closest(D, M)


[T_DM,d] = icp(M, D, 'verbose')
trprint(T_DM, 'rpy', 'radian')
T_DM = SE3(T_DM)

##
plot2(M', 'r.', 'MarkerSize', 20)
hold on
plot2( (inv(T_DM)*D)', 'b.', 'MarkerSize', 8)
hold off
xyzlabel

rvcprint.rvcprint(subfig='b')

## now with errors
randinit
D(:,randi(numcols(D), 40,1)) = []
D = [D 0.1*rand[2,19]+0.1]
D = D + 0.01*randn(size(D))


[T_DM,d] = icp(M, D, 'verbose', 'plot', 'distthresh', 3)
trprint(T_DM, 'rpy', 'radian')
