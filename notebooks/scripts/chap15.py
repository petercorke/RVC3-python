# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from math import pi
np.set_printoptions(linewidth=120, formatter={'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)

from machinevisiontoolbox.base import *
from machinevisiontoolbox import *
from spatialmath.base import *
from spatialmath import *

# ------------------------------ #

# # 15.1 Position-Based Visual Servoing
#

camera = CentralCamera.Default(pose=SE3.Trans(1, 1, -2));

P = mkgrid(2, 0.5)

p = camera.project_point(P, objpose=SE3.Tz(1))

Te_C_G = camera.estpose(P, p, frame="camera");
Te_C_G.printline()

T_Cd_G = SE3.Tz(1);

T_delta = Te_C_G * T_Cd_G.inv();
T_delta.printline()

camera.pose = camera.pose * T_delta.interp1(0.05);

camera = CentralCamera.Default(pose = SE3.Trans(1, 1, -2));

T_Cd_G = SE3.Tz(1);

pbvs = PBVS(camera, P=P, pose_g=SE3.Trans(-1, -1, 2), pose_d=T_Cd_G, plotvol=[-1, 2, -1, 2, -3, 2.5])

pbvs.run(200);

pbvs.plot_p();     # plot image plane trajectory
pbvs.plot_vel();   # plot camera velocity
pbvs.plot_pose();  # plot camera trajectory

# # 15.2 Image-Based Visual Servoing
#

# ## 15.2.1 Camera and Image Motion
#

camera = CentralCamera.Default();

P = [1, 1, 5];

p0 = camera.project_point(P)

p_dx = camera.project_point(P, pose=SE3.Tx(0.1))

(p_dx - p0) / 0.1

(camera.project_point(P, pose=SE3.Tz(0.1) ) - p0) / 0.1

(camera.project_point(P, pose=SE3.Rx(0.1)) - p0) / 0.1

J = camera.visjac_p(p0, depth=5)

camera.flowfield([1, 0, 0, 0, 0, 0]);

camera.flowfield([0, 0, 1, 0, 0, 0]);

camera.flowfield([0, 0, 0, 0, 0, 1]);

camera.flowfield([0, 0, 0, 0, 1, 0]);

camera.visjac_p(camera.pp, depth=1)

camera.f = 20e-3;
camera.flowfield([0, 0, 0, 0, 1, 0]);

camera.f = 4e-3;
camera.flowfield([0, 0, 0, 0, 1, 0]);

J = camera.visjac_p(camera.pp, depth=1);

sp.linalg.null_space(J)

# ## 15.2.2 Controlling Feature Motion
#

camera = CentralCamera.Default(pose=SE3.Trans(1, 1, -2));

P = mkgrid(2, side=0.5, pose=SE3.Tz(3));

pd = 200 * np.array([[-1, -1, 1, 1], [-1, 1, 1, -1]]) + np.c_[camera.pp]

p = camera.project_point(P)

e = pd - p

J = camera.visjac_p(p, depth=1);

lmbda = 0.1;
v = lmbda * np.linalg.pinv(J) @ e.flatten(order="F")

camera.pose = camera.pose @ SE3.Delta(v);

camera = CentralCamera.Default(pose=SE3.Trans(1, 1, -3) * SE3.Rz(0.6));
ibvs = IBVS(camera, P=P, p_d=pd);

ibvs.run(25);

ibvs.plot_p();     # plot image plane trajectory
ibvs.plot_vel();   # plot camera velocity
ibvs.plot_pose();  # plot camera trajectory 

ibvs.plot_jcond();

%run -m IBVS-main -H

out

plt.plot(out.t, out.y2)

plt.plot(out.clock0.t, out.clock0.x)

# ## 15.2.3 Estimating Feature Depth
#

ibvs = IBVS(camera, P=P, p_d=pd, depth=1);
ibvs.run(50)
ibvs = IBVS(camera, P=P, p_d=pd, depth=10);
ibvs.run(50)

ibvs = IBVS(camera, P=P, p_d=pd, depthest=True);
ibvs.run()

# ## 15.2.4 Performance Issues
#

pbvs.pose_0 = SE3.Trans(-2.1, 0, -3) * SE3.Rz(5*pi/4);
pbvs.run()

ibvs.pose_0 = pbvs.pose_0;
ibvs.run()
ibvs.plot_p();

ibvs.pose_0 = SE3.Tz(-1) * SE3.Rz(2);
ibvs.run(50)

ibvs.pose_0 = SE3.Tz(-1) * SE3.Rz(pi);
ibvs.run(10)

# # 15.3 Using Other Image Features
#

# ## 15.3.1 Line Features
#

P = circle([0, 0, 3], 0.5, resolution=3);

ibvs = IBVS_l.Example(camera);  # quick problem setup
ibvs.run()

# ## 15.3.2 Ellipse Features
#

P = circle([0, 0, 3], 0.5, resolution=10);

p = camera.project_point(P, pose=camera.pose, retinal=True);

x, y = p
A = np.column_stack([y**2, -2*x*y, 2*x, 2*y, np.ones(x.shape)]);
b = -(x**2);
E, *_ = np.linalg.lstsq(A, b, rcond=None)

plane = [0, 0, 1, -3];  # plane Z=3
J = camera.visjac_e(E, plane);
J.shape

ibvs = IBVS_e.Example();  # quick problem setup
ibvs.run()

# ## 15.3.3 Photometric Features
#

# # 15.4 Wrapping Up
#

# ## 15.4.1 Further Reading
#

# ## 15.4.2 Exercises
#

