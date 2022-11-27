#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import open3d as o3d
from spatialmath.base import trotx, transl


bunny_pcd = PointCloud.Read('data/bunny.ply')

bunny_pcd.disp(block=False, file=rvcprint.outfile(subfig='a', format='png'))
print(bunny_pcd)

#----------------------------------------------------------------------- #

voxel_grid = bunny_pcd.voxel_grid(voxel_size=0.01)

view = {
			"front" : [ -0.33625724752753799, 0.64479728158672767, 0.68641644003008151 ],
			"lookat" : [ -0.014689899999999992, 0.1079874, -0.001873600000000003 ],
			"up" : [ 0.27548123082049963, 0.7643220044666903, -0.58302827114441302 ],
			"zoom" : 0.69999999999999996
		}

voxel_grid.disp(block=False, file=rvcprint.outfile(subfig='b', format='png'), mesh_show_wireframe=True, **view)


#----------------------------------------------------------------------- #

obb = bunny_pcd.get_oriented_bounding_box()
print(obb.extent, obb.center)

# show normals
pcd = bunny_pcd.downsample_voxel(voxel_size=0.01)
pcd.normals(radius=0.1, max_nn=30)
pcd.disp(point_show_normal=True, block=False, file=rvcprint.outfile(subfig='c', format='png'))

