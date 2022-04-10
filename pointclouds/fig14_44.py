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

(model + data).write("fig4_44a.pcd")

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

(model + T.inv() * data).write("fig4_44b.pcd")
