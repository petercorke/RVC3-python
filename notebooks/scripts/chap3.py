# # 3.1 Time-Varying Pose
#

# ## 3.1.1 Rate of Change of Orientation
#

# ## 3.1.2 Rate of Change of Pose
#

# ## 3.1.3 Transforming Spatial Velocities
#

aTb = SE3.Tx(-2) * SE3.Rz(-pi/2) * SE3.Rx(pi/2);

bV = [1, 2, 3, 4, 5, 6];

aJb = aTb.jacob();
aJb.shape
aV = aJb @ bV

aV = aTb.Ad() @ [1, 2, 3, 0, 0, 0]

aV = aTb.Ad() @ [0, 0, 0, 1, 0, 0]

aV = aTb.Ad() @ [1, 2, 3, 1, 0, 0]

# ## 3.1.4 Incremental Rotation
#

rotx(0.001)

import time
Rexact = np.eye(3); Rapprox = np.eye(3);  # null rotation
w = np.array([1, 0, 0]);   # rotation of 1rad/s about x-axis
dt = 0.01;            # time step
t0 = time.process_time();
for i in range(100):  # exact integration over 100 time steps
  Rexact = Rexact @ trexp(skew(w*dt));       # update by composition
print(time.process_time() - t0)
t0 = time.process_time();
for i in range(100):  # approximate integration over 100 time steps
  Rapprox = Rapprox + Rapprox @ skew(w*dt);  # update by addition
print(time.process_time() - t0)

np.linalg.det(Rapprox) - 1

np.linalg.det(Rexact) - 1

tr2angvec(trnorm(Rexact))
tr2angvec(trnorm(Rapprox))

# ## 3.1.5 Incremental Rigid-Body Motion
#

# # 3.2 Accelerating Bodies and Reference Frames
#

# ## 3.2.1 Dynamics of Moving Bodies
#

J = np.array([[ 2, -1, 0],
              [-1,  4, 0],
              [ 0,  0, 3]]);

orientation = UnitQuaternion();  # identity quaternion
w = 0.2 * np.array([1, 2, 2]);

dt = 0.05;  # time step
def update():
  global orientation, w
  for t in np.arange(0, 10, dt):
     wd = -np.linalg.inv(J) @ (np.cross(w, J @ w))  # (3.12)
     w += wd * dt
     orientation *= UnitQuaternion.EulerVec(w * dt)
     yield orientation.R
tranimate(update())

# ## 3.2.2 Transforming Forces and Torques
#

bW = [1, 2, 3, 0, 0, 0];

aW = aTb.inv().Ad().T @ bW

# ## 3.2.3 Inertial Reference Frame
#

# # 3.3 Creating Time-Varying Pose
#

# ## 3.3.1 Smooth One-Dimensional Trajectories
#

traj = quintic(0, 1, np.linspace(0, 1, 50));

traj.plot();

quintic(0, 1, np.linspace(0, 1, 50), qd0=10, qdf=0);

qd = traj.qd;
qd.mean() / qd.max()

traj = trapezoidal(0, 1, np.linspace(0, 1, 50));
traj.plot();

traj.qd.max()

traj1_2 = trapezoidal(0, 1, np.linspace(0, 1, 50), V=1.2);
traj2_0 = trapezoidal(0, 1, np.linspace(0, 1, 50), V=2);

# ## 3.3.2 Multi-Axis Trajectories
#

traj = mtraj(trapezoidal, [0, 2], [1, -1], 50);

traj.plot();

q = np.array([T.t, T.rpy()])

# ## 3.3.3 Multi-Segment Trajectories
#

via = SO2(30, unit="deg") * np.array([[-1, 1, 1, -1, -1], [1, 1, -1, -1, 1]]);
traj0 = mstraj(via.T, dt=0.2, tacc=0, qdmax=[2, 1]);

xplot(traj0.q[:, 0], traj0.q[:, 1], color="red");

traj2 = mstraj(via.T, dt=0.2, tacc=2, qdmax=[2, 1]);

len(traj0), len(traj2)

# ## 3.3.4 Interpolation of Orientation in 3D
#

R0 = SO3.Rz(-1) * SO3.Ry(-1);
R1 = SO3.Rz(1) * SO3.Ry(1);

rpy0 = R0.rpy(); rpy1 = R1.rpy();

traj = mtraj(quintic, rpy0, rpy1, 50);

pose = SO3.RPY(traj.q);
len(pose)

pose.animate();

q0 = UnitQuaternion(R0); q1 = UnitQuaternion(R1);

qtraj = q0.interp(q1, 50);
len(qtraj)

qtraj.animate()

# ### 3.3.4.1 Direction of Rotation
#

q0 = UnitQuaternion.Rz(-2); q1 = UnitQuaternion.Rz(2);
q = q0.interp(q1, 50);
q.animate()

q = q0.interp(q1, 50, shortest=True);
q.animate()

# ## 3.3.5 Cartesian Motion in 3D
#

T0 = SE3.Trans([0.4, 0.2, 0]) * SE3.RPY(0, 0, 3);
T1 = SE3.Trans([-0.4, -0.2, 0.3]) * SE3.RPY(-pi/4, pi/4, -pi/2);

T0.interp(T1, 0.5)

Ts = T0.interp(T1, 51);

len(Ts)

Ts.animate()

Ts[25]

P = Ts.t;
P.shape

xplot(P, labels="x y z");

rpy = Ts.rpy();
xplot(rpy, labels="roll pitch yaw");

Ts = T0.interp(T1, trapezoidal(0, 1, 50).q);

Ts = ctraj(T0, T1, 50);

# # 3.4 Application: Inertial Navigation
#

# ## 3.4.1 Gyroscopes
#

# ### 3.4.1.1 How Gyroscopes Work
#

# ### 3.4.1.2 Estimating Orientation
#

from imu_data import IMU
true, _ = IMU()

orientation = UnitQuaternion();  # identity quaternion

for w in true.omega[:-1]:
  next = orientation[-1] @ UnitQuaternion.EulerVec(w * true.dt);
  orientation.append(next);
len(orientation)

orientation.animate(time=true.t)

xplot(true.t, orientation.rpy(), labels="roll pitch yaw");

# ## 3.4.2 Accelerometers
#

# ### 3.4.2.1 How Accelerometers Work
#

# ### 3.4.2.2 Estimating Pose and Body Acceleration
#

# ## 3.4.3 Magnetometers
#

# ### 3.4.3.1 How Magnetometers Work
#

# ### 3.4.3.2 Estimating Heading
#

# ## 3.4.4 Inertial Sensor Fusion
#

from imu_data import IMU
true, imu = IMU()

q = UnitQuaternion();
for wm in imu.gyro[:-1]:
  q.append(q[-1] @ UnitQuaternion.EulerVec(wm * imu.dt))

xplot(true.t, q.angdist(true.orientation), color="red");

kI = 0.2; kP = 1;
b = np.zeros(imu.gyro.shape);
qcf = UnitQuaternion();
data = zip(imu.gyro[:-1], imu.accel[:-1], imu.magno[:-1]);
for k, (wm, am, mm) in enumerate(data):
  qi = qcf[-1].inv()
  sR = np.cross(am, qi * true.g) + np.cross(mm, qi * true.B)
  wp = wm - b[k,:] + kP * sR
  qcf.append(qcf[k] @ UnitQuaternion.EulerVec(wp * imu.dt))
  b[k+1,:] = b[k,:] - kI * sR * imu.dt

xplot(true.t, qcf.angdist(true.orientation), color="blue");

# # 3.5 Wrapping Up
#

# ## 3.5.1 Further Reading
#

# ## 3.5.2 Exercises
#

