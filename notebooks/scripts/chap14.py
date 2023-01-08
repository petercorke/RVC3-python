# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from math import pi
np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)

from machinevisiontoolbox.base import *
from machinevisiontoolbox import *
from spatialmath.base import *
from spatialmath import *

from RVC3.examples.ransac_line import ransac_line

# ------------------------------ #
 
# # 14.1 Point Feature Correspondence
#

view1 = Image.Read("eiffel-1.png")
view2 = Image.Read("eiffel-2.png")

hf = view1.Harris(nfeat=150)
view1.disp(darken=True); hf.plot();

sf = view1.SIFT().sort().filter(minscale=10)[:150]
view1.disp(darken=True); sf.plot(filled=True, color="y", alpha=0.3)

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

plt.hist(matches.distance, cumulative=True, density=True);

m = sf1.match(sf2, thresh=20);

m = sf1.match(sf2, sort=True)[:10];

m = sf1.match(sf2, ratio=0.8)

m = sf1.match(sf2, crosscheck=True)

# # 14.2 Geometry of Multiple Views
#

camera1 = CentralCamera(name="camera 1", f=0.002, imagesize=1000, 
                        rho=10e-6, pose=SE3.Tx(-0.1)*SE3.Ry(0.4))

camera2 = CentralCamera(name="camera 2", f=0.002, imagesize=1000, 
                        rho=10e-6, pose=SE3.Tx(0.1)*SE3.Ry(-0.4))

ax = plotvol3([-0.4, 0.6, -0.5, 0.5, -0.2, 1]);
camera1.plot(ax=ax, scale=0.15, shape="camera", frame=True, color="blue");
camera2.plot(ax=ax, scale=0.15, shape="camera", frame=True, color="red");

P=[0.5, 0.1, 0.8];

plot_sphere(0.03, P, color="blue");

p1 = camera1.plot_point(P)
p2 = camera2.plot_point(P)

e1 = camera1.plot_point(camera2.centre, "kd")
e2 = camera2.plot_point(camera1.centre, "kd")

# ## 14.2.1 The Fundamental Matrix
#

F = camera1.F(camera2)

e2h(p2).T @ F @ e2h(p1)

np.linalg.matrix_rank(F)

e1h = sp.linalg.null_space(F);
e1h.T

e1 = h2e(e1h)

e2h = sp.linalg.null_space(F.T);
e2 = h2e(e2h)

camera2.plot_epiline(F, p1, color="red")

camera1.plot_epiline(F.T, p2, color="red");

# ## 14.2.2 The Essential Matrix
#

E = camera1.E(F)

T_1_2 = camera1.decomposeE(E);
T_1_2.printline(orient="camera")

T_1_2_true = camera1.pose.inv() * camera2.pose;
T_1_2_true.printline(orient="camera")

T_1_2_true.t / np.linalg.norm(T_1_2_true.t)

Q = [0, 0, 10];

camera1.project_point(Q).T

for T in T_1_2:
 print(camera1.project_point(Q, pose=T).T)

T = camera1.decomposeE(E, Q);
T.printline(orient="camera")

# ## 14.2.3 Estimating the Fundamental Matrix from Real Image Data
#

P = np.random.uniform(low=-1, high=1, size=(3, 10)) + np.c_[0, 0, 3].T;

p1 = camera1.project_point(P);
p2 = camera2.project_point(P);

F, resid = CentralCamera.points2F(p1, p2)
resid

np.linalg.matrix_rank(F)

camera2.plot_point(P);

camera2.plot_epiline(F, p1, color="red")

p2[:,[5, 6]] = p2[:,[6, 5]];

_, resid = CentralCamera.points2F(p1, p2);
resid

CentralCamera.epidist(F, p1[:, 0], p2[:,0])
CentralCamera.epidist(F, p1[:, 5], p2[:,5])

F, resid, inliers = CentralCamera.points2F(p1, p2, method="ransac", 
                                           confidence=0.99, seed=0);
resid

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
plt.plot(x, m * x + c, 'r--');
params, inliers = ransac_line(x, y)
params
inliers
sum([not inlier for inlier in inliers])

F, resid = matches.estimate(CentralCamera.points2F, method="ransac", 
                            confidence=0.99, seed=0);

matches
matches[:10].list()

matches.inliers.subset(100).plot(color="g");

matches.outliers.subset(100).plot(color="red")

camera = CentralCamera();
camera.disp(view1);

camera.plot_epiline(F.T, matches.inliers.subset(20).p2, color="black");

epipole = h2e(sp.linalg.null_space(F))
camera.plot_point(epipole, "wd");

# ## 14.2.4 Planar Homography
#

T_grid = SE3.Tz(1) * SE3.Rx(0.1) * SE3.Ry(0.2);
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
plot_sphere(0.05, P, color="blue");
plot_sphere(0.05, Q, color="red");
camera1.plot(color="blue", frame=True);
camera2.plot(color="red", frame=True);

p1 = camera1.plot_point(np.hstack((P, Q)), "o");

p2 = camera2.plot_point(np.hstack((P, Q)), "o");

p2h = homtrans(H, p1);

camera2.plot_point(p2h, "+");

np.linalg.norm(homtrans(H, p1) - p2, axis=0)

H, resid, inliers = CentralCamera.points2H(p1, p2, method="ransac");
resid
inliers

T, normals = camera1.decomposeH(H);
T.printline(orient="camera")

(camera1.pose.inv() * camera2.pose).printline(orient="camera")

camera1.pose.inv() * T_grid

normals[1].T

walls_l = Image.Read("walls-l.png", reduce=2);
walls_r = Image.Read("walls-r.png", reduce=2);

sf_l = walls_l.SIFT();
sf_r = walls_r.SIFT();

matches = sf_l.match(sf_r);

H, resid = matches.estimate(CentralCamera.points2H, confidence=0.9, seed=0)
matches

walls_l.disp();
plot_point(matches.inliers.p1, "r.");

not_plane = matches.outliers;

# # 14.3 Sparse Stereo
#

# ## 14.3.1 3D Triangulation
#

matches = sf_l.match(sf_r)
F, resid = matches.estimate(CentralCamera.points2F, confidence=0.99, seed=0);

matches = matches.inliers  # keep only the inliers

camera = CentralCamera();
camera.disp(walls_l);
camera.plot_epiline(F.T, matches.subset(40).p2, "yellow");

f = walls_l.metadata("FocalLength")

name = walls_l.metadata("Model")

camera = CentralCamera(name=name, imagesize=walls_l.shape, 
                       f=f/1000, rho=2*1.5e-6)

E = camera.E(F)

T_1_2 = camera.decomposeE(E, [0, 0, 10]);
T_1_2.printline(orient="camera")

t = T_1_2.t;
s = 0.3 / t[0]  # estimate of translation scale factor
T_1_2.t = s * t  # scaled translation
T_1_2.printline(orient="camera")

ray1 = camera.ray(matches[0].p1)

ray2 = camera.ray(matches[0].p2, pose=T_1_2)

P, e = ray1.closest_to_line(ray2);
P

e

ray1 = camera.ray(matches.p1);
ray2 = camera.ray(matches.p2, pose=T_1_2);

len(ray1)

P, e = ray1.closest_to_line(ray2);
P.shape

z = P[2, :];
z.mean()

np.median(e)
e.max()

plotvol3();
plt.plot(P[0,:], P[1,:], P[2,:], '.', markersize=2);

walls_pcd = PointCloud(P)
walls_pcd.transform(SE3.Rx(pi));  # make y-axis upward

walls_pcd.disp()

walls_pcd = walls_pcd.remove_outlier(nb_points=10, radius=0.2)

colors = []
for m in matches:
  colors.append(walls_l.image[int(m.p1[1]), int(m.p1[0]), :])
pcd = SE3.Rx(pi) * PointCloud(P, colors=np.array(colors).T)
pcd.disp()

p1_reproj = camera.project_point(P[:, 0]);
p2_reproj = camera.project_point(P[:, 0], pose=T_1_2);

(p1_reproj - matches[0].p1).T
(p2_reproj - matches[0].p2).T

bundle = BundleAdjust(camera)

view0 = bundle.add_view(SE3(), fixed=True);
view1 = bundle.add_view(SE3.Tx(0.3));

for (Pj, mj) in zip(P[:, ::4].T, matches[::4]):
  landmark = bundle.add_landmark(Pj)             # add vertex
  bundle.add_projection(view0, landmark, mj.p1)  # add edge
  bundle.add_projection(view1, landmark, mj.p2)  # add edge

bundle

bundle.plot()

x = bundle.getstate();
x.shape

x[6:12]

x[12:15]

bundle.errors(x)

# p, A, B = camera.derivatives(t, r, P);

x_new, resid = bundle.optimize(x);

bundle.setstate(x_new);

bundle.views[1].pose.printline(orient="camera")

T_1_2.printline(orient="camera")

bundle.landmarks[0].P

e = np.sqrt(bundle.getresidual());
e.shape

np.median(e, axis=1)

np.max(e, axis=1)

# # 14.4 Dense Stereo Matching
#

rocks_l = Image.Read("rocks2-l.png", reduce=2)
rocks_r = Image.Read("rocks2-r.png", reduce=2)

# rocks_l.stdisp(rocks_r)

disparity, *_ = rocks_l.stereo_simple(rocks_r, hw=3, drange=[40, 90]);

disparity.disp(colorbar=True);

disparity, similarity, DSI = rocks_l.stereo_simple(rocks_r, hw=3, drange=[40, 90])

DSI.shape

np.argmax(DSI, axis=2);

similarity_values = np.max(DSI, axis=2);

plt.plot(DSI[439, 138, :], "o-");

# ## 14.4.1 Peak Refinement
#

disparity_refined, A = Image.DSI_refine(DSI)

# ## 14.4.2 Stereo Failure Modes
#

# ### 14.4.2.1 Multiple peaks
#

# ### 14.4.2.2 Weak matching
#

similarity.disp();

similarity.choose("blue", similarity < 0.6).disp();

plt.hist(similarity.view1d(), 100, (0, 1), cumulative=True, density=True);

# ### 14.4.2.3 Broad peak
#

# ### 14.4.2.4 Quantifying Failure Modes
#

status = np.ones(disparity.shape);

U, V = disparity.meshgrid()
status[np.isnan(disparity.image)] = 5   # no similarity computed
status[U <= 90] = 2                     # no overlap
status[similarity.image < 0.6] = 3      # weak match
status[A.image >= -0.1] = 4             # broad peak

plt.imshow(status);

(status == 1).sum() / status.size * 100

disparity_valid = disparity.choose(0, status!=1)

# ### 14.4.2.5 Slicing the DSI
#

Image(DSI[100, :, :].T).disp();

# ### 14.4.2.6 Summary
#

# ### 14.4.2.7 Advanced Stereo Matching
#

disparity_BM = rocks_l.stereo_BM(rocks_l, hw=3, drange=[40, 90], speckle=(200, 2))
disparity_BM.disp();

rocks_l.stereo_SGBM(rocks_l, hw=3, drange=[40, 90], speckle=(200, 2)).disp();

# ### 14.4.2.8 3D Reconstruction
#

di = disparity_BM.image * 2 + 274;

U, V = disparity_BM.meshgrid();
u0, v0 = disparity.centre;
f = 3740;   # pixels, according to Middlebury website
b = 0.160;  # m, according to Middlebury website
X = b * (U - u0) / di; Y = b * (V - v0) / di; Z = f * b / di;

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, Z)
ax.view_init(-100, -100)

cam = CentralCamera(f=f, imagesize=rocks_l.shape);
pcd = PointCloud(Z, image=rocks_l, camera=cam, depth_trunc=1.9)
pcd *= SE3.Rx(pi);  # make y-axis upward

pcd.disp()

# ## 14.4.3 Image Rectification
#

walls_l = Image.Read('walls-l.png', reduce=2)
walls_r = Image.Read('walls-r.png', reduce=2)

sf_l = walls_l.SIFT()
sf_r = walls_r.SIFT()

matches = sf_l.match(sf_r);

F, resid = matches.estimate(CentralCamera.points2F, 
                            method="ransac", confidence=0.95);

H_l, H_r = walls_l.rectify_homographies(matches, F)

walls_l_rect = walls_l.warp_perspective(H_l)
walls_r_rect = walls_r.warp_perspective(H_r)

# walls_l_rect.stdisp(walls_r_rect)

walls_l_rect.stereo_SGBM(walls_r_rect, hw=7, drange=[180, 530], speckle=(50, 2)).disp();

# # 14.5 Anaglyphs
#

walls_l.anaglyph(walls_r, "rc").disp();


# # 14.7 Point Clouds
#

bunny_pcd = PointCloud.Read('data/bunny.ply')
bunny_pcd.disp(block=False)

pcd = bunny_pcd.voxel_grid(voxel_size=0.01).disp(block=False)

pcd = bunny_pcd.downsample_voxel(voxel_size=0.01)

pcd.normals(radius=0.1, max_nn=30)
pcd.disp(block=False)

# ## 14.7.1 Fitting a Plane
#

pcd = walls_pcd
plane, plane_pcd, pcd = pcd.segment_plane(distance_threshold=0.05, seed=0)
plane

plane_pcd

plane, plane_pcd, pcd = pcd.segment_plane(distance_threshold=0.05, seed=0)
plane

# ## 14.7.2 Matching Two Sets of Points
#

model = bunny_pcd.downsample_random(0.1, seed=0)

data = SE3.Trans(0.3, 0.4, 0.5) * SE3.Rz(50, unit="deg") * bunny_pcd.downsample_random(0.05, seed=-1);

model.paint([0, 0, 1])  # blue
data.paint([1, 0, 0])   # red
(model + data).disp(block=False)

T, status = model.ICP(data, max_correspondence_distance=1, 
                max_iteration=2000, relative_fitness=0, relative_rmse=0)
T.printline()

(model + T.inv() * data).disp(block=False)

# # 14.8 Applications
#

# ## 14.8.1 Perspective Correction
#

notredame = Image.Read("notre-dame.png");
notredame.disp();

picked_points = plt.ginput(4);

p1 = np.array(picked_points).T;

p1 = np.array([
        [ 44.1364,   94.0065,  537.8506,  611.8247], 
        [377.0654,  152.7850,  163.4019,  366.4486]]);

plot_polygon(p1, filled=True, color="y", alpha=0.4, linewidth=2);
plot_point(p1, "yo");

mn = p1.min(axis=1);
mx = p1.max(axis=1);
p2 = np.array([[mn[0], mn[0], mx[0], mx[0]], [mx[1], mn[1], mn[1], mx[1]]]);

plot_polygon(p2, "k--", close=True, linewidth=2);

H, _ = CentralCamera.points2H(p1, p2, method="leastsquares")
H

notredame.warp_perspective(H).disp();

f = notredame.metadata("FocalLength")

cam = CentralCamera(imagesize=notredame.shape, f=f/1000, sensorsize=[7.18e-3, 5.32e-3])

pose, normals = cam.decomposeH(H)
pose.printline(orient="camera")

normals[0].T

# ## 14.8.2 Image Mosaicing
#

images = ImageCollection("mosaic/aerial2-*.png", mono=True);

composite = Image.Zeros(2_000, 2_000)

composite.paste(images[0], (0, 0));

next_image = images[1]
sf_c = composite.SIFT()
sf_next= next_image.SIFT()
match = sf_c.match(sf_next);

H, _ = match.estimate(CentralCamera.points2H, "ransac", confidence=0.99);
H

tile, topleft, corners = next_image.warp_perspective(H, inverse=True, tile=True)

composite.paste(tile, topleft, method="blend");

# ## 14.8.3 Visual Odometry
#

left = ZipArchive("bridge-l.zip", filter="*.pgm", mono=True, dtype="uint8", 
                  maxintval=4095, roi=[20, 750, 20, 480]);
len(left)

for image in images:
  image.disp(reuse=True, block=0.05)

fig, ax = plt.subplots()
for image in left:
   ax.clear()                           # clear the axes
   image.disp(ax=ax)                    # display the image
   features = image.ORB(nfeatures=20)   # compute ORB features
   features = features.plot();          # display ORB features
   plt.pause(0.05)                      # small delay

right = ZipArchive("bridge-r.zip", mono=True, dtype="uint8", 
                   maxintval=4095, roi=[20, 750, 20, 480]);

# %run -m visodom

ts = np.loadtxt(left.open("timestamps.dat"));

plt.plot(np.diff(ts));



