import numpy as np
from numpy.core.numeric import zeros_like
import open3d as o3d
import matplotlib.pyplot as plt
from spatialmath.base import trotx
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', reduce=1)
R = Image.Read('rocks2-r.png', reduce=1)

disparity = L.stereo_BM(R, 6, [2*40, 2*90], (200, 2))
disparity.disp(grid=True)

# map to world coordinates
b = 0.160 # m
f = 3740 *2  # pixels
di = disparity.image + 274*2
U, V = L.meshgrid()

u0 = L.width / 2
v0 = L.height / 2

X = b * (U - u0) / di
Y = b * (V - v0) / di
Z = f * b / di

Image(Z).disp()

# xyz = np.column_stack((X.ravel(), Y.rqvel(), Z.ravel()))
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(xyz)


# print(pcd)
# o3d.visualization.draw_geometries([pcd])

rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    o3d.geometry.Image(L.image), 
    o3d.geometry.Image(Z), 
    depth_scale=1.0, depth_trunc=1.9, convert_rgb_to_intensity=False)
print(rgbd_image)

pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
    rgbd_image,
    o3d.camera.PinholeCameraIntrinsic(L.width, L.height, f, f, *L.centre))
print(pcd)
# pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
#     rgbd_image,
#     o3d.camera.PinholeCameraIntrinsic(
#         o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))


# Flip it, otherwise the pointcloud will be upside down
# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
pcd.transform(trotx(np.pi))
o3d.visualization.draw_geometries([pcd])