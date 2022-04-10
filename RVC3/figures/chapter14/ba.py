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


walls_l = Image.Read("walls-l.png", reduce=2);
walls_r = Image.Read("walls-r.png", reduce=2);
sf_l = walls_l.SIFT();
sf_r = walls_r.SIFT();

matches = sf_l.match(sf_r); ##


## deleted the plane fitting, reassigns matches

# Stereo Vision


# Sparse Stereo

F, resid = matches.estimate(CentralCamera.points2F, confidence=0.99, seed=0);
in100 = matches.inliers.subset(100);


f = walls_l.metadata("FocalLength")
name = walls_l.metadata("Model")
camera = CentralCamera(name=name, imagesize=walls_l.shape, f=f/1000, rho=2*1.5e-6)

E = camera.E(F)
T_1_2 = camera.decomposeE(E, [0, 0, 10]);
T_1_2.printline(orient="camera")
t = T_1_2.t;
T_1_2.t = 0.3 * t / t[0]
T_1_2.printline(orient="camera")

r1 = camera.ray(in100.p1);
r2 = camera.move(T_1_2).ray(in100.p2);
P, e = r1.closest_to_line(r2);
P.shape
z = P[2, :];
e.mean()
e.max()
print('emean', e.mean())
print('emax', e.max())
print('zmean', z.mean())
walls_l.disp();
plot_point(in100.p1, "y+", textcolor="y", text=(" {1:.1f}", z));


# Bundle Adjustment

p1 = camera.project_point(P);
p2 = camera.move(T_1_2).project_point(P);
e = np.linalg.norm(np.hstack((p1-in100.p1, p2-in100.p2)), axis=0);
print('emean', e.mean())
print('emax', e.max())
ba = BundleAdjust(camera)
view0 = ba.add_view(SE3(), 'fixed');
view1 = ba.add_view(T_1_2);
# camera2 = camera.move(T_1_2)
for match in in100: ##
  ray1 = camera.ray(match.p1)
  ray2 = camera.move(T_1_2).ray(match.p2)
  P, d = ray1.closest_to_line(ray2)
  landmark = ba.add_landmark(P)
  ba.add_projection(view0, landmark, match.p1)
  ba.add_projection(view1, landmark, match.p2)
print(ba) ##
print(len(ba.views))
print(ba.views[1])

plotvol3()
ba.plot()
x = ba.getstate();
x.shape
x[6:12]
x[12:15]
print('ba errors', ba.errors(x))
x_new, resid = ba.optimize(x);

print(ba) ##
print(len(ba.views))
print(ba.views[1])

ba.setstate(x_new);
print(len(ba.views))
print(ba.views[1])
ba.views[1].pose.printline(orient="camera")
T_1_2.printline(orient="camera")
ba.landmarks[5].P
ba.plot()
e = np.sqrt(ba.getresidual());
e.shape
e.median()
np.where(e[0, :] > 1)
k = np.argmax(e[0, :])
e[0, k]

# Depth from Structured Light

import open3d as o3d
