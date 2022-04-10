# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import cv2 as cv

import ansitable
ansitable.options(unicode=False)

from spatialmath import *
from spatialmath.base import *
BasePoseMatrix._color=False
from roboticstoolbox import *

from spatialmath.base import *
import math
from math import pi

from machinevisiontoolbox import *
from machinevisiontoolbox.base import *

np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})



np.random.seed(0)
cv.setRNGSeed(0)

# ------------------------------ #


# Feature Correspondence

view1 = Image.Read("eiffel2-1.png")
view2 = Image.Read("eiffel2-2.png")
hf = view1.Harris(nfeat=150)
view1.disp(darken=True); hf.plot();
sf = view1.SIFT().sort().filter(minscale=10)[:150]
view1.disp(darken=True); sf.plot("gs")
hf[0].descriptor.shape
hf[0].distance(hf[1], metric="ncc")
sf[0].descriptor.shape
sf[0].distance(sf[1], metric="L2")
sf1 = view1.SIFT()
sf2 = view2.SIFT()
matches = sf1.match(sf2);
len(matches)
matches[:5].list()
matches.subset(100).plot(color="yellow")
c = matches.correspondence();
c[:, :5]
m = sf1.match(sf2);
plt.hist(m.distance, cumulative=True, density=True);
m = sf1.match(sf2, thresh=20);
m = sf1.match(sf2, sort=True)[:10];
m = sf1.match(sf2, ratio=0.8)
m = sf1.match(sf2, crosscheck=True)

# Geometry of Multiple Views

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4);
camera1 = CentralCamera(name="camera 1", f=0.002, imagesize=1000, rho=10e-6, pose=T1)
T2 = SE3(0.1, 0,0)*SE3.Ry(-0.4);
camera2 = CentralCamera(name="camera 2", f=0.002, imagesize=1000, rho=10e-6, pose=T2)
ax = plotvol3([-0.4, 0.6, -0.5, 0.5, -0.2, 1]);
camera1.plot(ax=ax, scale=0.15, shape="camera", frame=True, color="blue");
camera2.plot(ax=ax, scale=0.15, shape="camera", frame=True, color="red");
P=[0.5, 0.1, 0.8];
plot_sphere(0.03, P, color="blue");
p1 = camera1.plot_point(P)
p2 = camera2.plot_point(P)
e1 = camera1.plot_point(camera2.centre, "kd")
e2 = camera2.plot_point(camera1.centre, "kd")

# The Fundamental Matrix

F = camera1.F(camera2)
e2h(p2).T @ F @ e2h(p1)
np.linalg.matrix_rank(F)
e1h = sp.linalg.null_space(F);
e1h.T
e1 = h2e(e1h)
e2h = sp.linalg.null_space(F.T);
e2 = h2e(e2h)
camera2.plot_epiline(F, p1, color="red")
camera1.plot_epiline(F.T, p2, color="r");

# The Essential Matrix

E = camera1.E(F)
pose_1_2 = camera1.decomposeE(E);
pose_1_2.printline(orient="camera")
pose_1_2_true = (camera1.pose.inv() * camera2.pose);
pose_1_2_true.printline(orient="camera")
pose_1_2_true.t / np.linalg.norm(pose_1_2_true.t)
Q = [0, 0, 10];
camera1.project_point(Q).T
camera1.project_point(Q, pose=pose_1_2[0]).T
camera1.project_point(Q, pose=pose_1_2[2]).T
pose = camera1.decomposeE(E, Q);
pose.printline(orient="camera")

# Estimating the Fundamental Matrix from Real Image Data

P = np.random.uniform(low=-1, high=1, size=(3, 10)) + np.c_[0, 0, 3].T;
p1 = camera1.project_point(P);
p2 = camera2.project_point(P);
F, resid = CentralCamera.points2F(p1, p2)
resid
np.linalg.matrix_rank(F)
camera2.plot_point(P);
camera2.plot_epiline(F, p1, color="r")
p2[:,[5, 6]] = p2[:,[6, 5]];
_, resid = CentralCamera.points2F(p1, p2);
resid
CentralCamera.epidist(F, p1[:, 0], p2[:,0])
CentralCamera.epidist(F, p1[:, 5], p2[:,5])
F, resid, inliers = CentralCamera.points2F(p1, p2, method="ransac", confidence=0.99);
inliers
F, resid, inliers = CentralCamera.points2F(matches.p1, matches.p2,
                                           method="ransac", confidence=0.99);
resid
sum(inliers) / len(inliers)
x = np.arange(11);
y = 3 * x - 10;
nbad = 4;
np.random.seed(1)  # set the random number generator seed
bad = np.random.choice(len(x), nbad, replace=False)
y[bad] = y[bad] + np.random.rand(nbad) * 10
import scipy as sp
m, c, *_ = sp.stats.linregress(x, y)
plt.plot(x, m * x + c, 'b--');
F, resid = matches.estimate(CentralCamera.points2F, method="ransac", confidence=0.99, seed=0);
matches
matches[:10].list()
matches.inliers.subset(100).plot(color="g");
matches.outliers.subset(100).plot(color="r")
camera = CentralCamera();
camera.disp(view1);
camera.plot_epiline(F.T, matches.inliers.subset(20).p2, color="black");
epipole = h2e(sp.linalg.null_space(F))
camera.plot_point(epipole, "wd");

# Planar Homography

T_grid = SE3(0,0,1) * SE3.Rx(0.1) * SE3.Ry(0.2);
P = mkgrid(3, 1.0, pose=T_grid);
p1 = camera1.plot_point(P, "o");
p2 = camera2.plot_point(P, "o");
H, resid = CentralCamera.points2H(p1, p2)
H
p2b = homtrans(H, p1);
camera2.plot_point(p2b, "+");
p1b = homtrans(np.linalg.inv(H), p1);
Q = np.array([
  [-0.2302,   -0.0545,    0.2537],
  [ 0.3287,    0.4523,    0.6024],
  [ 0.4000,    0.5000,    0.6000] ]);
plotvol3([-1, 1, -1, 1, 0, 2]);
plot_sphere(0.05, P, "b");
plot_sphere(0.05, Q, "r");
camera1.plot(color="b", label=True);
camera2.plot(color="r", label=True);
p1 = camera1.plot_point(np.hstack((P, Q)), "o");
p2 = camera2.plot_point(np.hstack((P, Q)), "o");
p2h = homtrans(H, p1);
camera2.plot_point(p2h, "+");
np.linalg.norm(homtrans(H, p1) - p2, axis=0)
H, resid, inliers = CentralCamera.points2H(p1, p2, method="ransac");
resid
inliers
pose, normals = camera1.decomposeH(H);
pose.printline(orient="camera")
(T1.inv() * T2).printline()
T1.inv() * T_grid
walls_l = Image.Read("walls-l.png", reduce=2);
walls_r = Image.Read("walls-r.png", reduce=2);
sf_l = walls_l.SIFT();
sf_r = walls_r.SIFT();
matches = sf_l.match(sf_r);
H, resid = matches.estimate(CentralCamera.points2H, confidence=0.9, seed=0)
matches
walls_l.disp();
plot_point(matches.inliers.p1, "r.");
matches = matches.outliers;

# # Sparse Stereo

# matches = sf_l.match(sf_r)
# F, resid = matches.estimate(CentralCamera.points2F, confidence=0.99, seed=0);
# in100 = matches.inliers.subset(100);
# camera = CentralCamera();
# camera.disp(walls_l);
# camera.plot_epiline(F.T, in100.subset(40).p2, "b");
# f = walls_l.metadata("FocalLength")
# name = walls_l.metadata("Model")
# camera = CentralCamera(name=name, imagesize=walls_l.shape, f=f/1000, rho=2*1.5e-6)
# E = camera.E(F)
# T_1_2 = camera.decomposeE(E, [0, 0, 10]);
# T_1_2.printline(orient="camera")
# t = T_1_2.t;
# T_1_2.t = 0.3 * t / t[0]
# T_1_2.printline(orient="camera")
# r1 = camera.ray(in100[0].p1)
# r2 = camera.move(T_1_2).ray(in100[0].p2)
# P, e = r1.closest_to_line(r2);
# P
# e
# r1 = camera.ray(in100.p1);
# r2 = camera.move(T_1_2).ray(in100.p2);
# len(r1)
# P, e = r1.closest_to_line(r2);
# P.shape
# z = P[2, :];
# z.mean()
# e.mean()
# e.max()
# walls_l.disp();
# plot_point(in100.p1, "y+", textcolor="y", text=(" {1:.1f}", z));

# # Bundle Adjustment

# ba = BundleAdjust(camera)
# view0 = ba.add_view(SE3(), 'fixed');
# view1 = ba.add_view(T_1_2);
# camera2 = camera.move(T_1_2)
# for match in in100.subset(100):
#   ray1 = camera.ray(match.p1)
#   ray2 = camera2.ray(match.p2)
#   P, d = ray1.closest_to_line(ray2)
#   landmark = ba.add_landmark(P)
#   ba.add_projection(view0, landmark, match.p1)
#   ba.add_projection(view1, landmark, match.p2)
# ba
# ba.plot()
# x = ba.getstate();
# x.shape
# x[6:12]
# x[12:15]
# ba.errors(x)
# x_new, resid = ba.optimize(x);
# ba.setstate(x_new);
# ba.views[1].pose.printline(orient="camera")
# T_1_2.printline(orient="camera")
# ba.landmarks[5].P
# ba.plot()
# e = np.sqrt(ba.getresidual());
# e.shape
# np.median(e)
# np.where(e[0, :] > 1)
# k = np.argmax(e[0, :])
# e[0, k]

# # Dense Stereo Matching

# rocks_l = Image.Read('rocks2-l.png', reduce=2)
# rocks_r = Image.Read('rocks2-r.png', reduce=2)
# rocks_l.stdisp(rocks_r)
# disparity, *_ = rocks_l.stereo_simple(rocks_r, hw=3, drange=[40, 90]);
# disparity.disp(colorbar=True);
# disparity, similarity, DSI = rocks_l.stereo_simple(rocks_r, hw=3, drange=[40, 90])
# DSI.shape
# np.argmax(DSI, axis=2);
# np.max(DSI, axis=2);
# plt.plot(DSI[439, 138, :], "o-");

# # Peak Refinement

# disparity_refined, A = Image.DSI_refine(DSI)

# # Stereo Failure Modes


# # Multiple peaks


# # Weak matching

# similarity.disp();
# similarity.choose("blue", similarity < 0.6).disp();
# plt.hist(similarity.view1d(), 100, (0, 1), cumulative=True, density=True);

# # Broad peak


# # Quantifying Failure Modes

# status = np.ones(disparity.shape);
# U, V = disparity.meshgrid()
# status[np.isnan(disparity.image)] = 5   # no similarity computed
# status[U <= 90] = 2                     # no overlap
# status[similarity.image < 0.6] = 3      # weak match
# status[A.image >= -0.1] = 4             # broad peak
# plt.imshow(status);
# (status == 1).sum() / status.size * 100
# Image(DSI[100, :, :].T).disp();

# # Summary


# # Advanced Stereo Matching

# disparity_BM = rocks_l.stereo_BM(rocks_l, hw=3, drange=[40, 90], speckle=(200, 2)).disp();
# rocks_l.stereo_SGBM(rocks_l, hw=3, drange=[40, 90], speckle=(200, 2)).disp();

# 3D Reconstruction

# di = disparity.image + 274;
# di = disparity.image;
# U, V = disparity.meshgrid();
# u0, v0 = disparity.centre
# b = 0.160;
# X = b * (U - u0) / di; Y = b * (V - v0) / di; Z = 3740 * b / di;

# # Image Rectification

# walls_l = Image.Read('walls-l.png', reduce=2)
# walls_r = Image.Read('walls-r.png', reduce=2)
# sf_l = walls_l.SIFT()
# sf_r = walls_r.SIFT()
# matches = sf_l.match(sf_r);
# F, resid = matches.estimate(CentralCamera.points2F,
#                             method="ransac", confidence=0.95);
# H_l, H_r = walls_l.rectify_homographies(matches, F)
# walls_l_rect = walls_l.warp_perspective(H_l)
# walls_r_rect = walls_r.warp_perspective(H_r)
# walls_l_rect.stdisp(walls_r_rect)
# walls_l_rect.stereo_SGBM(walls_r_rect, hw=7, drange=[180, 530], speckle=(50, 2)).disp();

# Anaglyphs

walls_l.anaglyph(walls_r, "rc").disp();

# Other Depth Sensing Technologies


# Depth from Structured Light


# Depth from Time-Of-Flight


# Point Clouds

# import open3d as o3d

# # Fitting a Plane

# T = SE3(1,2,3) * SE3.RPY(0.3, 0.4, 0.5);
# P = mkgrid(10, 1, pose=T);
# P += np.random.normal(scale=0.02, size=P.shape);
# x0 = P.mean(axis=1)
# P = P - x0.reshape((3, 1));
# J = P @ P.T
# e, x = np.linalg.eig(J);
# e
# i = np.argmin(e)
# n = x[:, i]
# T.R[:, 2]

# Matching Two Sets of Points


# Applications


# Perspective Correction

notredame = Image.Read("notre-dame.png");
notredame.disp();
p1 = np.array([
                [ 44.1364,   94.0065,  537.8506,  611.8247],
                [377.0654,  152.7850,  163.4019,  366.4486]]);
plot_poly(p1, filled=True, color="y", alpha=0.4, linewidth=2);
plot_point(p1, "yo");
mn = p1.min(axis=1);
mx = p1.max(axis=1);
p2 = np.array([[mn[0], mn[0], mx[0], mx[0]], [mx[1], mn[1], mn[1], mx[1]]]);
plot_poly(p2, "k--", close=True, linewidth=2);
H, _ = CentralCamera.points2H(p1, p2, method='leastsquares')
H
notredame.warp_perspective(H).disp();
f = notredame.metadata("FocalLength")
cam = CentralCamera(imagesize=notredame.shape, f=f/1000, sensorsize=[7.18e-3, 5.32e-3])
pose, normals = cam.decomposeH(H)
pose.printline(orient="camera")
normals[0].T

# Image Mosaicing

# images = ImageCollection("mosaic/aerial2-*.png", mono=True);
# composite = Image.Zeros(2_000, 2_000)
# composite.paste(images[0], (0, 0));
# next_image = images[1]
# sf_c = composite.SIFT()
# sf_next= next_image.SIFT()
# match = sf_c.match(sf_next);
# H, _ = match.estimate(CentralCamera.points2H, "ransac");
# H
# tile, topleft, corners = next_image.warp_perspective(H, inverse=True, tile=True)
# composite.paste(tile, topleft, "blend");

# Visual Odometry

# left = ZipArchive("bridge-l.zip", mono=True, dtype="uint8", maxintval=4095, roi=[20, 750, 20, 480]);
# len(left)
# for image in images:
#   image.disp(reuse=True, block=0.05)
# right = ZipArchive("bridge-r.zip", mono=True, dtype="uint8", maxintval=4095, roi=[20, 750, 20, 480]);
# ts = np.loadtxt(mvtb_path_to_datafile('data/timestamps.dat'));
# plt.plot(np.diff(ts));

# Wrapping Up


# Further Reading


# Resources


# Exercises

