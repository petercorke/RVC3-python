# # 16.1 XY/Z-Partitioned IBVS
#

%run -m IBVS-partitioned-main -H

# # 16.2 IBVS Using Polar Coordinates
#

camera = CentralCamera.Default(pose=SE3.Tz(-2)*SE3.Rz(pi))
P = mkgrid(2, 0.5, pose=SE3.Tz(2))
ibvs = IBVS_polar(camera, lmbda=0.1, P=P, pose_d=SE3.Tz(1), depth=2, graphics=False)

ibvs.run()

ibvs.plot_p()
ibvs.plot_pose()

# # 16.3 IBVS for a Spherical Camera
#

camera = SphericalCamera(pose=SE3.Trans(0.3, 0.3, -2)*SE3.Rz(0.4))
P = mkgrid(2, side=1.5, pose=SE3.Tz(0.5))

ibvs = IBVS_sph(camera, P=P, pose_d=SE3.Tz(-1.5), verbose=False, graphics=False)

ibvs.run()

# # 16.4 Applications
#

# ## 16.4.1 Arm-Type Robot
#

%run -m IBVS-arm-main -H

plt.plot(out.clock1.t, out.clock1.x)

# ## 16.4.2 Mobile Robot
#

# ### 16.4.2.1 Holonomic Mobile Robot
#

camera = CentralCamera.Default(f=0.002);

T_B_C = SE3.Trans(0.2, 0.1, 0.3) * SE3.Rx(-pi/4);

P = np.array([[0, 1, 2], [0, -1, 2]]).T;

%run -m IBVS-holonomic-main -H

# ### 16.4.2.2 Nonholonomic Mobile Robot
#

%run -m IBVS-nonholonomic-main -H

# ## 16.4.3 Aerial Robot
#

%run -m IBVS-quadrotor-main -H

# # 16.5 Wrapping Up
#

# ## 16.5.1 Further Reading
#

# ## 16.5.2 Resources
#

# ## 16.5.3 Exercises
#

