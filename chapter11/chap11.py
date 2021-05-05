## RVC2: Chapter 11 - Image Formation

import numpy as np
import scipy as sp
from math import pi
from spatialmath import SE3
from spatialmath.base import e2h, h2e, plot_sphere
from machinevisiontoolbox import *

# ## 11.1.2  Modelling a perspective camera

# camera = CentralCamera(f=0.015)

# P = [0.3, 0.4, 3.0]

# camera.project(P)

# camera.project(P, pose=SE3(-0.5, 0, 0))

# ## 11.1.3  Discrete image plane

# camera = CentralCamera(f=0.015, rho=10e-6,
#     imagesize=[1280, 1024], pp=[640, 512], name='mycamera')

# camera.project(P)

# ## 11.1.4  camera matrix

# camera.K

# camera.C

# camera.fov() * 180 / math.pi

# ## 11.1.5  Projecting points

# P = mkgrid(3, 0.2, pose=SE3(0, 0, 1.0))

# P[:, 0:3]

# camera.project(P)

# camera.plot(P)

# Tcamera = SE3(-1, 0, 0.5) * SE3.Ry(0.9)

# camera.plot(P, pose=Tcamera)

# camera.project([1, 0, 0, 0], pose=Tcamera)

# p = camera.plot(P, pose=Tcamera)

# p[:, :3]

# cube = mkcube(0.2, pose=SE3(0, 0, 1))

# camera.plot(cube)

# X, Y, Z = mkcube(0.2, pose=SE3(0, 0, 1), edge=True)

# camera.mesh(X, Y, Z)

# T_camera = SE3(-1, 0, 0.5) * SE3.Ry(0.8)
# camera.mesh(X, Y, Z, pose=T_camera)

# # camera.clf()
# X, Y, Z = mkcube(0.2, edge=True)
# for theta in np.linspace(0, 2 * pi, 100):
#     T_cube = SE3(0, 0, 1.5)  * SE3.RPY(theta * np.r_[1.1, 1.2, 1.3])
#     camera.clf()
#     camera.mesh(X, Y, Z, objpose=T_cube)
#     # plt.pause(0.1)

# ## 11.1.6  Lens distortion

# k1 = 0; k2 = 0; k3 = 0; p1 = 0; p2 = 0;  # dummy values

# camera = CentralCamera(f=0.015, rho=10e-6, 
#     imagesize=[1280, 1024], pp=[512, 512],
#     distortion=[k1, k2, k3, p1, p2])

# ## 11.2.1  Homogeneous transformation approach

# P = mkcube(0.2)

# T_unknown = SE3(0.1, 0.2, 1.5) * SE3.RPY(0.1, 0.2, 0.3)

# camera = CentralCamera(f=0.015, rho=10e-6, imagesize=[1280, 1024], \
#     noise=0.05)

# p = camera.project(P, objpose=T_unknown)

# C, resid = CentralCamera.camcald(P, p)

# ## 11.2.2  Decomposing the camera calibration matrix

# o = sp.linalg.null_space(C)

# h2e(o)
# T_unknown.inv().t

# est = CentralCamera.InvCamcal(C)

# est.f / est.rho[0]

# camera.f / camera.rho[1]

# (T_unknown * est.pose).printline()

# # plt.clf()
# est.plot_camera(scale=0.3)
# plot_sphere(P, 0.03, color='r')
# SE3().plot(frame='T', color='b', length=0.3)
# ax = plt.gca()
# ax.set_xlim3d(-0.9, 0.9)
# ax.set_ylim3d(-0.9, 0.9)
# ax.set_zlim3d(-1.5, 0.3)



# ## 11.2.3  Pose estimation

# camera = CentralCamera(f=0.015, rho=10e-6, imagesize=[1280, 1024], pp=[640, 512])

# P = mkcube(0.2)

# T_unknown = SE3(0.1, 0.2, 1.5) * SE3.RPY(0.1, 0.2, 0.3)
# T_unknown.printline()

# p = camera.project(P, objpose=T_unknown)

# T_est = camera.estpose(P, p).printline()

# ## 11.2.4  camera calibration toolbox

# #calib_gui

# #visualize_distortions


# ## 11.3.1  Fisheye lens camera

# camera = FishEyeCamera(
#             projection='equiangular',
#             rho=10e-6,
#             imagesize=[1280, 1024]
#             )

# X, Y, Z = mkcube(0.2, centre=[0.2, 0, 0.3], edge=True)

# camera.mesh(X, Y, Z, color='k')


# ## 11.3.2  Catadioptric camera

# camera = CatadioptricCamera(
#             projection='equiangular',
#             rho=10e-6,
#             imagesize=[1280, 1024],
#             maxangle=pi/4
#         )
     
# X, Y, Z = mkcube(1, centre=[1, 1, 0.8], edge=True)

# camera.mesh(X, Y, Z, color='k')


# ## 11.3.3  Spherical camera

# camera = SphericalCamera()

# X, Y, Z = mkcube(1, centre=[2, 3, 1], edge=True)

# camera.mesh(X, Y, Z, color='k')


# ## 11.4.1  Mapping wide angle images to the sphere
# # Set the parameters of the fisheye camera that took the picture, then load 
# # the image

# u0 = 528.1214; v0 = 384.0784; l = 2.7899; m = 996.4617;

# fisheye = Image.Read('fisheye_target.png', dtype='float', grey=True)
# fisheye.disp()


# n = 500
# theta_range = np.linspace(0, pi, n)
# phi_range = np.linspace(-pi, pi, n)

# Phi, Theta = np.meshgrid(phi_range, theta_range)

# r = (l + m) * np.sin(Theta) / (l - np.cos(Theta))
# Us = r * np.cos(Phi) + u0
# Vs = r * np.sin(Phi) + v0

# spherical = fisheye.interp2d(Us, Vs)
# # im_spherical = f(theta_range, phi_range)

# spherical.disp(badcolor='red')
# # plt.show(block=True)


# # sphere
# R = 1
# x = R * np.sin(Theta) * np.cos(Phi)
# y = R * np.sin(Theta) * np.sin(Phi)
# z = R * np.cos(Theta)

# plt.close('all')

# # create 3d Axes
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# img = spherical.colorize()

# ax.plot_surface(x, y, z, facecolors=img.image, cstride=1, rstride=1)
# # ax.plot_surface(x, y, z, facecolors=img.image, cstride=1, rstride=1) # we've already pruned ourselves

# ax.view_init(azim=-143.0, elev=-9)

# # plt.show(block=True)

# ## 11.4.2  Mapping from the sphere to a perspective image

# W = 1000
# m = W / 2 / math.tan(np.radians(45 / 2))

# l = 0

# u0 = W / 2; v0 = W/2;

# Uo, Vo = np.meshgrid(np.arange(W), np.arange(W))

# U0 = Uo - u0
# V0 = Vo - v0
# phi = np.arctan2(V0, U0)
# r = np.sqrt(U0 ** 2 + V0 ** 2)

# Phi_o = phi
# Theta_o = pi - np.arctan(r / m)

# # perspective = interp2d(Phi, Theta, im_spherical, Phi_o, Theta_o)
# perspective = spherical.interp2d(Phi_o, Theta_o, Phi, Theta)
# perspective.disp(badcolor='red')
# # plt.show(block=True)

# # dth = theta_range[1] - theta_range[0]
# # dph = phi_range[1] - phi_range[0]

# # spherical2 = spherical.roll(int(0.9/dth), int(-1.5/dph))
# # perspective = spherical2.interp2d(Phi_o, Theta_o, Phi, Theta)
# # perspective.disp(badcolor='red')

# def sphere_rotate(sph, T):

#     nr, nc = sph.shape

#     # theta spans [0, pi]
#     theta_range = np.linspace(0, pi, nr)

#     # phi spans [-pi, pi]
#     phi_range = np.linspace(-pi, pi, nc)

#     # build the plaid matrices
#     Phi, Theta = np.meshgrid(phi_range, theta_range)

#     # convert the spherical coordinates to Cartesian
#     x = np.sin(Theta) * np.cos(Phi)
#     y = np.sin(Theta) * np.sin(Phi)
#     z = np.cos(Theta)

#     # convert to 3xN format
#     p = np.array([x.flatten(), y.flatten(), z.flatten()])

#     # transform the points
#     p = T * p

#     # convert back to Cartesian coordinate matrices
#     x = p[0, :].reshape(x.shape)
#     y = p[1, :].reshape(x.shape)
#     z = p[2, :].reshape(x.shape)

#     nTheta = np.arccos(z)
#     nPhi = np.arctan2(y, x)

#     #warp the image
#     return sph.interp2d(nPhi, nTheta, Phi, Theta)


# perspective.disp(badcolor='red', title='view2')


## 11.6.1  Projecting 3D lines and quadrics
from spatialmath import Plucker

L = Plucker.PQ([0, 0, 1], [1, 1, 1])

L.w

camera = CentralCamera()
l = camera.project(L)

camera.plot(l)


##
camera = CentralCamera(f=0.015, imagesize=[1024, 1024], rho=10e-6, pose=SE3(0.2,0.1, -5)*SE3.Rx(0.2))

Q = np.diag([1, 1, 1, -1])

Qs = np.linalg.inv(Q) * np.linalg.det(Q) # adjugate
cs = camera.C @ Qs @ camera.C.T
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