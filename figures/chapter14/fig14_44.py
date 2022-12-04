#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import open3d as o3d
from spatialmath.base import trotx, transl

bunny_pcd = PointCloud.Read('data/bunny.ply')

# random downsample
# downpcd = pcd.random_down_sample(0.01)
# o3d.visualization.draw_geometries([downpcd])

model = bunny_pcd.downsample_random(0.1, seed=0)
data = bunny_pcd.downsample_random(0.05, seed=-1)
# data = model.copy()
# data.transform(SE3(0.3, 0.4, 0.5) * SE3.Rz(1.0))
data *= SE3(0.3, 0.4, 0.5) * SE3.Rz(1.0)

model.paint([0, 0, 1])  # blue
data.paint([1, 0, 0])  # red


(model + data).disp(block=False, file=rvcprint.outfile(subfig='a', format='png'))

import open3d as o3d

o3d.io.write_point_cloud("fig4_44a.ply", (model + data).pcd)

#----------------------------------------------------------------------- #

T, status = model.ICP(data, max_correspondence_distance=1, max_iteration=2000, relative_fitness=0, relative_rmse=0)

print(status)
T.printline()
T.inv().printline()

# data.transform(T.inv())

view = {
			"front" : [ -0.59722996483481749, 0.19877636899178081, 0.77704846968116881 ],
			"lookat" : [ -0.016745428423718761, 0.1098642, -0.0015208075222352124 ],
			"up" : [ 0.062601193125750354, 0.97740058168073718, -0.20191382703863806 ],
			"zoom" : 0.69999999999999996
		}

(model + T.inv() * data).disp(**view, block=False, file=rvcprint.outfile(subfig='b', format='png'))

# (rtb) >>> import cv2 as cv

# (rtb) >>> a=cv.ppf_match_3d_ICP(20)

# (rtb) >>> a.registerModelToScene(data, model)
# https://stackoverflow.com/questions/56809980/how-to-import-all-the-points-from-a-pcd-file-into-a-2d-python-array
# http://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html?highlight=icp
# load bunny
# M = bunny
# T_unknown = SE3(0.2, 0.2, 0.1) * SE3.rpy(0.2, 0.3, 0.4)
# D = T_unknown * M

# clf
# plot2(M', 'r.', 'MarkerSize', 20)
# hold on
# plot2(D', 'b.', 'MarkerSize', 8)
# hold off
# xyzlabel
# rvcprint.rvcprint(subfig='a')


# corresp = closest(D, M)


# [T_DM,d] = icp(M, D, 'verbose')
# trprint(T_DM, 'rpy', 'radian')
# T_DM = SE3(T_DM)

# ##
# plot2(M', 'r.', 'MarkerSize', 20)
# hold on
# plot2( (inv(T_DM)*D)', 'b.', 'MarkerSize', 8)
# hold off
# xyzlabel

# rvcprint.rvcprint(subfig='b')

# ## now with errors
# randinit
# D(:,randi(numcols(D), 40,1)) = []
# D = [D 0.1*rand[2,19]+0.1]
# D = D + 0.01*randn(size(D))


# [T_DM,d] = icp(M, D, 'verbose', 'plot', 'distthresh', 3)
# trprint(T_DM, 'rpy', 'radian')
