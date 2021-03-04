%% Matlab commands extracted from /Users/corkep/doc/svn/book/src/localization/chap.tex
format compact
close all
clear
clc

%% sect 6.1 dead reckoning
V = diag([0.02, 0.5*pi/180].^2);

veh = Bicycle('covar', V)

randinit
odo = veh.step(1, 0.3)

veh.x'

veh.f([0 0 0], odo)

veh.add_driver( RandomPath(10) )

veh.run()

%% sec 6.1.2
veh.Fx( [0,0,0], [0.5, 0.1] )

P0 = diag([0.005, 0.005, 0.001].^2);

ekf = EKF(veh, V, P0);

randinit
ekf.run(1000);

clf
veh.plot_xy()

hold on
ekf.plot_xy('r')

P700 = ekf.history(700).P

sqrt(P700(1,1))

ekf.plot_ellipse('g')

%% sec 6.2 map based localization

randinit
map = LandmarkMap(20, 10)

map.plot()

W = diag([0.1, 1*pi/180].^2);

sensor = RangeBearingSensor(veh, map, 'covar', W)


[z,i] = sensor.reading()

map.landmark(17)

randinit
map = LandmarkMap(20);
veh = Bicycle('covar', V);
veh.add_driver( RandomPath(map.dim) );
sensor = RangeBearingSensor(veh, map, 'covar', W, 'angle', ...
[-pi/2 pi/2], 'range', 4, 'animate');
ekf = EKF(veh, V, P0, sensor, W, map);

ekf.run(1000);
map.plot()
veh.plot_xy();
ekf.plot_xy('r');
ekf.plot_ellipse('k')

%% sec 6.3 creating a map

randinit
map = LandmarkMap(20);
veh = Bicycle(); % error free vehicle
veh.add_driver( RandomPath(map.dim) );
W = diag([0.1, 1*pi/180].^2);
sensor = RangeBearingSensor(veh, map, 'covar', W);
ekf = EKF(veh, [], [], sensor, W, []);

ekf.run(1000);

map.plot();
ekf.plot_map('g');
veh.plot_xy('b');


ekf.landmarks(:,6)

ekf.x_est(19:20)'

ekf.P_est(19:20,19:20)

%% sect 6.4 SLAM

randinit
P0 = diag([.01, .01, 0.005].^2);
map = LandmarkMap(20);
veh = Bicycle('covar', V);
veh.add_driver( RandomPath(map.dim) );
sensor = RangeBearingSensor(veh, map, 'covar', W);
ekf = EKF(veh, V, P0, sensor, W, []);

ekf.run(1000);

map.plot();
ekf.plot_map('g');
ekf.plot_xy('r');
veh.plot_xy('b');

%% sect 6.6 PG SLAM

syms xi yi ti xj yj tj xm ym tm assume real
xi_e = inv( SE2(xm, ym, tm) ) * inv( SE2(xi, yi, ti) ) * SE2(xj, yj, tj);
fk = simplify(xi_e.xyt);

jacobian ( fk, [xi yi ti] );
Ai = simplify (ans)

pg = PoseGraph('pg1.g2o')

pg.plot()

pg.optimize('animate')

pg = PoseGraph('killian-small.toro');

pg.plot()

pg.optimize('animate')


%% 6.7 particle filter
randinit
map = LandmarkMap(20);
W = diag([0.1, 1*pi/180].^2);
veh = Bicycle('covar', V);
veh.add_driver( RandomPath(10) );

V = diag([0.005, 0.5*pi/180].^2);
sensor = RangeBearingSensor(veh, map, 'covar', W);

Q = diag([0.1, 0.1, 1*pi/180]).^2;

L = diag([0.1 0.1]);

pf = ParticleFilter(veh, sensor, Q, L, 1000);

pf.run(1000);

map.plot();
veh.plot_xy('b');

pf.plot_xy('r');

plot(pf.std(1:100,:))

pf.plot_pdf()
