import numpy as np
from numpy.core.numeric import zeros_like
import open3d as o3d
import matplotlib.pyplot as plt
from spatialmath.base import trotx
from machinevisiontoolbox import *

walls_l = Image.Read('walls-l.png', reduce=2)
walls_r = Image.Read('walls-r.png', reduce=2)

sL = walls_l.SIFT()
sR = walls_r.SIFT()
matches = sL.match(sR)

F, resid = matches.estimate(CentralCamera.points2F,
    method='ransac', confidence=0.99, seed=0)
print(resid)
print(matches)

matches = matches.inliers

# iphone has 1.5um pixels, double for the image subsampling
cam = CentralCamera(f=4.15e-3, rho=2*1.5e-6)
# cam.disp(im1.mono(), darken=True)
# im1 = imono(im1)

E = cam.E(F)
print(E)

# these give solutions with same R, but different sign of t
# doesn't matter because next we normalize for tx = 0.3
T = cam.decomposeE(E)
T.printline(orient='camera')
print()
T = cam.decomposeE(E, np.r_[0, 0, 10])
T.printline(orient='camera')

T = SE3.Rt(T.R, 0.3 * T.t / T.t[0])
T.printline(orient='camera', label='FINAL')

lines1 = cam.ray(matches.p1)
lines2 = cam.move(T).ray(matches.p2)

P1, e = lines1.closest_to_line(lines2)
print(e.mean())
print(e.max())
print(P1[2,:].mean())

xyz = P1.T
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)
pcd, ind = pcd.remove_radius_outlier(nb_points=16, radius=0.2)

pcd.transform(trotx(np.pi))
o3d.visualization.draw_geometries([pcd])

plane_model, inliers = pcd.segment_plane(distance_threshold=0.05)
# distance_threshold=0.05,
#                                          ,
#                                          num_iterations=100)

inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
o3d.visualization.draw_geometries([inlier_cloud])


# F, resid = matches.estimate(CentralCamera.points2F, 
#     'ransac', confidence=0.95, seed=0)

# HL, HR = walls_l.rectify_homographies(matches, F)

# walls_l_rect = walls_l.warp_perspective(HL)
# walls_r_rect = walls_r.warp_perspective(HR)

# disparity = walls_l_rect.stereo_SGBM(walls_r_rect, 13, [180, 530], (50, 2))
# disparity.disp(grid=True, colorbar=dict(label='Disparity (pixels)'))

# f = 4.15e-3 / (2*1.5e-6)

# Z = f  / disparity.image

# Image(Z).disp()

# plt.show(block=True)


# print(f)

# rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
#     o3d.geometry.Image(walls_l.image), 
#     o3d.geometry.Image(Z), 
#     depth_scale=1.0, depth_trunc=6, convert_rgb_to_intensity=False)
# print(rgbd_image)

# pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
#     rgbd_image,
#     o3d.camera.PinholeCameraIntrinsic(walls_l.width, walls_l.height, f, f, *walls_l.centre))
# print(pcd)
# # pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
# #     rgbd_image,
# #     o3d.camera.PinholeCameraIntrinsic(
# #         o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))


# # Flip it, otherwise the pointcloud will be upside down
# # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
# pcd.transform(trotx(np.pi))
# o3d.visualization.draw_geometries([pcd])