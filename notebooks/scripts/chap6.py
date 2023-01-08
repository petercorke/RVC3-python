# # 6.1 Dead Reckoning using Odometry
#

# ## 6.1.1 Modeling the Robot
#

V = np.diag([0.02, np.deg2rad(0.5)]) ** 2;

robot = Bicycle(covar=V, animation="car")

odo = robot.step((1, 0.3))

robot.q

robot.f([0, 0, 0], odo)

robot.control = RandomPath(workspace=10)

robot.run(T=10);

# ## 6.1.2 Estimating Pose
#

robot.Fx([0, 0, 0], [0.5, 0.1])

x_sdev = [0.05, 0.05, np.deg2rad(0.5)];
P0 = np.diag(x_sdev) ** 2;

ekf = EKF(robot=(robot, V), P0=P0)

ekf.run(T=20);

robot.plot_xy(color="b")

ekf.plot_xy(color="r")

P150 = ekf.get_P(150)

np.sqrt(P150[0, 0])

ekf.plot_ellipse(filled=True, facecolor="g", alpha=0.3)

t = ekf.get_t();
pn = ekf.get_Pnorm();
plt.plot(t, pn);

# # 6.2 Localizing with a Landmark Map
#

map = LandmarkMap(20, workspace=10)

map.plot()

W = np.diag([0.1, np.deg2rad(1)]) ** 2;

sensor = RangeBearingSensor(robot=robot, map=map, covar=W,  
           angle=[-pi/2, pi/2], range=4, animate=True)

z, i = sensor.reading()
z
i

map[15]

map = LandmarkMap(20, workspace=10);
V = np.diag([0.02, np.deg2rad(0.5)]) ** 2
robot = Bicycle(covar=V, animation="car");
robot.control = RandomPath(workspace=map, seed=0)
W = np.diag([0.1, np.deg2rad(1)]) ** 2
sensor = RangeBearingSensor(robot=robot, map=map, covar=W, 
           angle=[-pi/2, pi/2], range=4, seed=0, animate=True);
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)]) ** 2;
ekf = EKF(robot=(robot, V), P0=P0, map=map, sensor=(sensor, W));

ekf.run(T=20)

map.plot()
robot.plot_xy();
ekf.plot_xy();
ekf.plot_ellipse()

# # 6.3 Creating a Landmark Map
#

map = LandmarkMap(20, workspace=10, seed=0);
robot = Bicycle(covar=V, animation="car");
robot.control = RandomPath(workspace=map);
W = np.diag([0.1, np.deg2rad(1)]) ** 2
sensor = RangeBearingSensor(robot=robot, map=map, covar=W, 
           range=4, angle=[-pi/2, pi/2], animate=True);
ekf = EKF(robot=(robot, None), sensor=(sensor, W));

ekf.run(T=100);

map.plot();
ekf.plot_map();
robot.plot_xy();

ekf.landmark(10)

ekf.x_est[24:26]

ekf.P_est[24:26, 24:26]

# # 6.4 Simultaneous Localization and Mapping
#

map = LandmarkMap(20, workspace=10);
W = np.diag([0.1, np.deg2rad(1)]) ** 2 
robot = Bicycle(covar=V, x0=(3, 6, np.deg2rad(-45)), 
          animation="car");
robot.control = RandomPath(workspace=map);
W = np.diag([0.1, np.deg2rad(1)]) ** 2
sensor = RangeBearingSensor(robot=robot, map=map, covar=W, 
           range=4, angle=[-pi/2, pi/2], animate=True);
P0 = np.diag([0.05, 0.05, np.deg2rad(0.5)]) ** 2;
ekf = EKF(robot=(robot, V), P0=P0, sensor=(sensor, W));

ekf.run(T=40);

map.plot();       # plot true map
robot.plot_xy();  # plot true path

ekf.plot_map();      # plot estimated landmark position
ekf.plot_ellipse();  # plot estimated covariance
ekf.plot_xy();       # plot estimated robot path

T = ekf.get_transform(map)

# # 6.5 Pose-Graph SLAM
#

import sympy
xi, yi, ti, xj, yj, tj = sympy.symbols("xi yi ti xj yj tj")
xm, ym, tm = sympy.symbols("xm ym tm")
xi_e = SE2(xm, ym, tm).inv() * SE2(xi, yi, ti).inv() \
     * SE2(xj, yj, tj);
fk = sympy.Matrix(sympy.simplify(xi_e.xyt()));

Ai = sympy.simplify(fk.jacobian([xi, yi, ti]))
Ai.shape

pg = PoseGraph("data/pg1.g2o");

pg.plot();

pg.optimize(animate=True)

pg = PoseGraph("data/killian-small.toro");

pg.plot();

pg.optimize()

# # 6.6 Sequential Monte-Carlo Localization
#

map = LandmarkMap(20, workspace=10);

V = np.diag([0.02, np.deg2rad(0.5)]) ** 2;
robot = Bicycle(covar=V, animation="car", workspace=map);
robot.control = RandomPath(workspace=map)

W = np.diag([0.1, np.deg2rad(1)]) ** 2;
sensor = RangeBearingSensor(robot, map, covar=W, plot=True);

R = np.diag([0.1, 0.1, np.deg2rad(1)]) ** 2;

L = np.diag([0.1, 0.1]);

pf = ParticleFilter(robot, sensor=sensor, R=R, L=L, nparticles=1000);

pf.run(T=10);

map.plot();
robot.plot_xy();

pf.plot_xy();

plt.plot(pf.get_std()[:100,:]);

pf.plot_pdf()

# # 6.7 Rao-Blackwellized SLAM
#

# # 6.8 Application: Lidar
#

# ## 6.8.1 Lidar-based Odometry
#

pg = PoseGraph("data/killian.g2o.zip", lidar=True);

[r, theta] = pg.scan(100);
r.shape
theta.shape

plt.clf()
plt.polar(theta, r);

p100 = pg.scanxy(100);
p101 = pg.scanxy(100);
p100.shape

T = pg.scanmatch(100, 101);
T.printline()

pg.time(101) - pg.time(100)

# ## 6.8.2 Lidar-based Map Building
#

og = OccupancyGrid(workspace=[-100, 250, -100, 250], cellsize=0.1, value=np.int32(0));
pg.scanmap(og, maxrange=40)
og.plot(cmap="gray")

# ## 6.8.3 Lidar-based Localization
#

# # 6.9 Wrapping Up
#

# ## 6.9.1 Further Reading
#

# ## 6.9.2 Exercises
#

