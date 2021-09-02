#! /usr/bin/env python3
## RVC2: Chapter 11 - Image Formation

import numpy as np
import scipy as sp
from math import pi
from spatialmath import SE3
from spatialmath.base import e2h, h2e, plot_sphere
from machinevisiontoolbox import *

## 11.1.2  Modelling a perspective camera

camera = CentralCamera(f=0.015)

P = [0.3, 0.4, 3.0]

camera.project_point(P)

camera.project_point(P, pose=SE3(-0.5, 0, 0))

## 11.1.3  Discrete image plane

camera = CentralCamera(f=0.015, rho=10e-6,
    imagesize=[1280, 1024], pp=[640, 512], name='mycamera')

camera.project_point(P)

## 11.1.4  camera matrix

camera.K

camera.C

camera.fov() * 180 / math.pi

## 11.1.5  Projecting points

P = mkgrid(3, 0.2, pose=SE3(0, 0, 1.0));
P.shape

P[:, 0:3]

camera.project_point(P)

camera.plot_point(P)

Tcamera = SE3(-1, 0, 0.5) * SE3.Ry(0.9)

camera.plot(P, pose=Tcamera)

camera.project_point([1, 0, 0, 0], pose=Tcamera)

p = camera.plot_point(P, pose=Tcamera)

p[:, :3]

cube = mkcube(0.2, pose=SE3(0, 0, 1))

camera.plot_point(cube)

X, Y, Z = mkcube(0.2, pose=SE3(0, 0, 1), edge=True)

camera.plot_wireframe(X, Y, Z)

T_camera = SE3(-1, 0, 0.5) * SE3.Ry(0.8)
camera.plot_wireframe(X, Y, Z, pose=T_camera)

# camera.clf()
X, Y, Z = mkcube(0.2, edge=True)
for theta in np.linspace(0, 2 * pi, 100):
    T_cube = SE3(0, 0, 1.5)  * SE3.RPY(theta * np.r_[1.1, 1.2, 1.3])
    camera.clf()
    camera.plot_wireframe(X, Y, Z, objpose=T_cube)
    plt.pause(0.1)

## 11.1.6  Lens distortion

k1 = 0; k2 = 0; k3 = 0; p1 = 0; p2 = 0;  # dummy values

camera = CentralCamera(f=0.015, rho=10e-6, 
    imagesize=[1280, 1024], pp=[512, 512],
    distortion=[k1, k2, k3, p1, p2])

## 11.2.1  Homogeneous transformation approach

P = mkcube(0.2)

T_unknown = SE3(0.1, 0.2, 1.5) * SE3.RPY(0.1, 0.2, 0.3)

camera = CentralCamera(f=0.015, rho=10e-6, imagesize=[1280, 1024], \
    noise=0.05)

p = camera.project_point(P, objpose=T_unknown)

C, resid = CentralCamera.points2C(P, p)

## 11.2.2  Decomposing the camera calibration matrix

o = sp.linalg.null_space(C)

h2e(o).T
T_unknown.inv().t

est = CentralCamera.decomposeC(C)

est.f / est.rho[0]

camera.f / camera.rho[1]

(T_unknown * est.pose).printline()

# plt.clf()
plotvol3([-0.9, 0.9, -0.9, 0.9, -1.5, 0.3])
est.plot_camera(scale=0.3)
plot_sphere(0.03, P, color='r')
SE3().plot(frame='T', color='b', length=0.3)


## 11.2.3  Pose estimation

camera = CentralCamera(f=0.015, rho=10e-6, imagesize=[1280, 1024], pp=[640, 512])

P = mkcube(0.2)

T_unknown = SE3(0.1, 0.2, 1.5) * SE3.RPY(0.1, 0.2, 0.3)
T_unknown.printline()

p = camera.project_point(P, objpose=T_unknown)

T_est = camera.estpose(P, p).printline()

## 11.2.4  camera calibration toolbox

#calib_gui

#visualize_distortions


## 11.3.1  Fisheye lens camera

camera = FishEyeCamera(
            projection='equiangular',
            rho=10e-6,
            imagesize=[1280, 1024]
            )

X, Y, Z = mkcube(0.2, centre=[0.2, 0, 0.3], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


## 11.3.2  Catadioptric camera

camera = CatadioptricCamera(
            projection='equiangular',
            rho=10e-6,
            imagesize=[1280, 1024],
            maxangle=pi/4
        )
     
X, Y, Z = mkcube(1, centre=[1, 1, 0.8], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


## 11.3.3  Spherical camera

camera = SphericalCamera()

X, Y, Z = mkcube(1, centre=[2, 3, 1], edge=True)

camera.plot_wireframe(X, Y, Z, color='k')


## 11.4.1  Mapping wide angle images to the sphere
# Set the parameters of the fisheye camera that took the picture, then load 
# the image

u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

fisheye = Image.Read('fisheye_target.png', dtype='float', grey=True)
fisheye.disp()


n = 500
theta_range = np.linspace(0, pi, n)
phi_range = np.linspace(-pi, pi, n)

Phi, Theta = np.meshgrid(phi_range, theta_range)

r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
Us = r * np.cos(Phi) + u0
Vs = r * np.sin(Phi) + v0

spherical = fisheye.interp2d(Us, Vs)
# im_spherical = f(theta_range, phi_range)

spherical.disp(badcolor='red')
# plt.show(block=True)


plt.close('all')

# create 3d Axes
ax = plotvol3()

plot_sphere(radius=1, ax=ax, filled=True, resolution=n, 
    facecolors=spherical.colorize().A, cstride=1, rstride=1)
ax.view_init(azim=-143.0, elev=-9)

# plt.show(block=True)

## 11.4.2  Mapping from the sphere to a perspective image

W = 1000
m = W / 2 / math.tan(np.radians(45 / 2))

l = 0

u0 = W / 2; v0 = W/2;

Uo, Vo = np.meshgrid(np.arange(W), np.arange(W))

U0 = Uo - u0; V0 = Vo - v0
phi = np.arctan2(V0, U0)
r = np.sqrt(U0 ** 2 + V0 ** 2)

Phi_o = phi
Theta_o = pi - np.arctan(r / m)

# perspective = interp2d(Phi, Theta, im_spherical, Phi_o, Theta_o)
perspective = spherical.interp2d(Phi_o, Theta_o, Phi, Theta)
perspective.disp(badcolor='red')


nPhi, nTheta = base.sphere_rotate(Phi, Theta, SE3.Ry(0.9)*SE3.Rz(-1.5))

# warp the image
spherical2 = spherical.interp2d(nPhi, nTheta, Phi, Theta)

perspective = spherical2.interp2d(Phi_o, Theta_o, Phi, Theta)
perspective.disp(badcolor='red', title='view2')


## 11.6.1  Projecting 3D lines and quadrics
from spatialmath import Plucker

L = Plucker.PQ([0, 0, 1], [1, 1, 1])

L.w

camera = CentralCamera()
l = camera.project(L)

camera.plot(l)


##
camera = CentralCamera(f=0.015, imagesize=1024, rho=10e-6, pose=SE3(0.2,0.1, -5)*SE3.Rx(0.2))

Q = np.diag([1, 1, 1, -1])

Qs = np.linalg.inv(Q) * np.linalg.det(Q) # adjugate
cs = camera.C() @ Qs @ camera.C().T
c = np.linalg.inv(cs) * np.linalg.det(cs)  # adjugate
print('c', c)

np.linalg.det(c[:2, :2])

E = c + c.T
xy = -np.linalg.inv(E[:2, :2]) @ E[:2, 2]
print(xy)
i = (-xy @ (c[:2, :2] @ xy))
print(f"{i:.4g}")

i = c[0,0] * xy[0] ** 2 + c[1,1] * xy[1] ** 2 + 2 * c[0,1] * xy[0] * xy[1]
i = np.abs(i)
from sympy import symbols, Matrix, Eq, plot_implicit
plt.figure()
s = c[2,2] + 1
# s ~ 2.5e6
base.plot_ellipse(-c[:2, :2],  scale=np.sqrt(i+c[2,2]), centre=xy)
plt.grid(True)

x, y = symbols('x y')
X = Matrix([[x, y, 1]])
ellipse = X * Matrix(c) * X.T
plot_implicit(Eq(ellipse[0], 1), (x, 0, 1024), (y, 0, 1024), )

plt.show(block=True)