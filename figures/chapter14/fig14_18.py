#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3
import spatialmath.base as smbase

im1 = Image.Read('walls-l.png', reduce=2) #'reduce', 2)
im2 = Image.Read('walls-r.png', reduce=2) #'reduce', 2)

s1 = im1.SIFT()
s2 = im2.SIFT()

m = s1.match(s2)
 
F, resid = m.estimate(CentralCamera.points2F,
    method='ransac', confidence=0.99, seed=0)
print(resid)
print(m)

m = m.inliers

# iphone has 1.5um pixels, double for the image subsampling
cam = CentralCamera(f=4.15e-3, rho=2*1.5e-6)
cam.disp(im1.mono(), darken=True)
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


# all rays
lines1 = cam.ray(m.p1)
lines2 = cam.ray(m.p2, pose=T)

P1, e = lines1.closest_to_line(lines2)
print(e.mean())
print(e.max())
print(P1[2,:].mean())


# cut and paste from the cmd-C option of the display window
view =		{
			"front" : [ -0.15389683183812766, 0.38981422161306334, 0.90794308069305141 ],
			"lookat" : [ 1.6937472708883625, -0.42990060582530487, -2.2990513793231413 ],
			"up" : [ 0.016206418242278857, 0.91976210722229923, -0.39214157918505949 ],
			"zoom" : 0.10666900634765612
		}

pcd = PointCloud(P1)
pcd.transform(SE3.Rx(np.pi))
pcd.disp(**view, block=False, file=rvcprint.outfile(subfig='a', format='png'))


colors = []
for mm in m:
    colors.append(im1.image[int(mm.p1[1]), int(mm.p1[0]), :])
pcd = PointCloud(P1, colors=np.array(colors).T)
print(pcd)
# pcd = pcd.remove_outlier(nb_points=16, radius=0.2)
# print(pcd)

pcd.transform(SE3.Rx(np.pi))
pcd.disp(**view, block=False, file=rvcprint.outfile(subfig='b', format='png'))

# smbase.plotvol3()
# plt.plot(P1[0,:], P1[1,:], P1[2,:], '.', markersize=2)
# plt.show(block=True)