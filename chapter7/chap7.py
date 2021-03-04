%% CHAPTER 7
format compact
close all
clear
clc

%% 7.1.1 planar 2D
import ETS2.*
a1 = 1;
E = Rz('q1') * Tx(a1)

E.fkine( 30, 'deg')

%BUG E.teach

a1 = 1; a2 = 1;
E = Rz('q1') * Tx(a1) * Rz('q2') * Tx(a2)

E.fkine( [30, 40], 'deg')

%BUG E.plot( [30, 40], 'deg')

E.structure

a1 = 1;
%BUG E = Rz('q1') * Tx(a1) * Tz('q2')

E.structure

%% 7.1.2 3D arms

import ETS3.*
L1 = 0; L2 = -0.2337; L3 = 0.4318; L4 = 0.0203; L5 = 0.0837; L6 = 0.4318;
E3 = Tz(L1) * Rz('q1') * Ry('q2') * Ty(L2) * Tz(L3) * Ry('q3') ...
* Tx(L4) * Ty(L5) * Tz(L6) * Rz('q4') * Ry('q5') * Rz('q6');

%BUG E3.fkine([0 0 0 0 0 0])


%% 7.1.2.1 DH params
L = Revolute('a', 1)

L.A(0.5)

L.type

L.a

L.offset = 0.5;
L.A(0)

robot = SerialLink( [ Revolute('a', 1) Revolute('a', 1) ], ...
'name', 'my robot')

robot.fkine([30 40], 'deg')

models

mdl_irb140

robot.edit

%% 7.1.2.2 POE

a1 = 1; a2 = 1;
TE0 = SE2(a1+a2, 0, 0);

S1 = Twist( 'R', [0 0] );
S2 = Twist( 'R', [a1 0] );

%BUG TE = S1.T(30, 'deg') * S2.T(40, 'deg') *TE0


%% 7.1.2.3 6-axis industrial

mdl_puma560

p560

TE = p560.fkine(qz)

p560.tool = SE3(0, 0, 0.2);

p560.fkine(qz)

p560.base = SE3(0, 0, 30*0.0254);
p560.fkine(qz)

p560.base = SE3(0,0,3) * SE3.Rx(pi);
p560.fkine(qz)

q=jtraj(qz, qr, 8);
q

T = p560.fkine(q);

about(T)

T(4)

%% 7.2.1.1 inv kine closed form

import ETS2.*
a1 = 1; a2 = 1;
E = Rz('q1') * Tx(a1) * Rz('q2') * Tx(a2)

syms q1 q2 real

TE = E.fkine( [q1, q2] )

syms x y real

e1 = x == TE.t(1)
e2 = y == TE.t(2)

[s1,s2] = solve( [e1 e2], [q1 q2] )

length(s2)

s2(1)

%% 7.2.1.2

pstar = [0.6; 0.7];
q = fminsearch( @(q) norm( E.fkine(q).t - pstar ), [0 0] )

E.fkine(q).print

%% 7.2.2 3D inv kine

mdl_puma560
qn
T = p560.fkine(qn)
qi = p560.ikine6s(T)
p560.fkine(qi)


qi = p560.ikine6s(T, 'ru')

p560.ikine6s( SE3(3, 0, 0) )


q = [0 pi/4 pi 0.1 0 0.2];

p560.ikine6s(p560.fkine(q), 'ru')

q(4)+q(6)

%% 7.2.2.2 numerical 3D

T = p560.fkine(qn)
qi = p560.ikine(T)

qn

p560.fkine(qi)

p560.plot(qi)

qi = p560.ikine2(T, 'q0', [0 0 3 0 0 0])

%% 7.2.2.3
mdl_cobra600

c600

T = SE3(0.4, -0.3, 0.2) * SE3.rpy(30, 40, 160, 'xyz', 'deg');

q = c600.ikine2(T, 'mask', [1 1 1 0 0 1])

Ta = c600.fkine(q);
Ta.print('xyz')

TT = c600.fkine(q);
clf
trplot(T, 'color', 'b')
hold on 
trplot(Ta, 'color', 'r')

%% 7.2.2.4 redundant

mdl_baxter

left

TE = SE3(0.8, 0.2, -0.2) * SE3.Ry(pi);

q = left.ikine2(TE)

left.fkine(q).print

%% 7.3.1 trajectories

T1 = SE3(0.4, 0.2, 0) * SE3.Rx(pi);
T2 = SE3(0.4, -0.2, 0) * SE3.Rx(pi/2);

q1 = p560.ikine6s(T1);
q2 = p560.ikine6s(T2);

t = [0:0.05:2]';

q = mtraj(@tpoly, q1, q2, t);

q = mtraj(@lspb, q1, q2, t);

q = jtraj(q1, q2, t);

[q,qd,qdd] = jtraj(q1, q2, t);

q = p560.jtraj(T1, T2, t)

p560.plot(q)

plot(t, q(:,2))

qplot(t, q);

T = p560.fkine(q);

p = T.transl;

about(p)

plot(p(1,:), p(2,:))

plot(t, T.torpy('xyz'))

%% 7.3.2 cartesian motion

Ts = ctraj(T1, T2, length(t));

plot(t, Ts.transl);

plot(t, Ts.torpy('xyz'));

qc = p560.ikine6s(Ts);

%% 7.3.3 kinematics in simulink

sl_jspace

%% 7.3.4 motion through singularity

T1 = SE3(0.5, 0.3, 0.44) * SE3.Ry(pi/2);
T2 = SE3(0.5, -0.3, 0.44) * SE3.Ry(pi/2);

Ts = ctraj(T1, T2, length(t));

qc = p560.ikine6s(Ts)

m = p560.maniplty(qc);

%% 7.3.5 config change

T = SE3(0.4, 0.2, 0) * SE3.Rx(pi);

qr = p560.ikine6s(T, 'ru');
ql = p560.ikine6s(T, 'lu');

q = jtraj(qr, ql, t);

p560.plot(q)

%% 7.4.2 determining DH params


s = 'Tz(L1) Rz(q1) Ry(q2) Ty(L2) Tz(L3) Ry(q3) Tx(L4) Ty(L5) Tz(L6) Rz(q4) Ry(q5) Rz(q6)'

dh = DHFactor(s);

dh

cmd = dh.command('puma')

robot = eval(cmd)

%% 7.4.3 MDH

L1 = RevoluteMDH('d', 1)

%% 7.5.1 writing

load hershey

B = hershey{'B'}

B.stroke

path = [ 0.25*B.stroke; zeros(1,numcols(B.stroke))];
k = find(isnan(path(1,:)))
path(:,k) = path(:,k-1); path(3,k) = 0.2;

traj = mstraj(path(:,2:end)', [0.5 0.5 0.5], [], path(:,1)', ...
0.02, 0.2);

about(traj)

numrows(traj) * 0.02

plot3(traj(:,1), traj(:,2), traj(:,3))

Tp = SE3(0.6, 0, 0) * SE3(traj) * SE3.oa( [0 1 0], [0 0 -1]);

q = p560.ikine6s(Tp);

p560.plot(q)

%% 7.5.2 walking


s = 'Rz(q1).Rx(q2).Ty(L1).Rx(q3).Tz(L2)';

dh = DHFactor(s);

dh.tool

dh.command('leg')

L1 = 0.1; L2 = 0.1;
leg = eval( dh.command('leg') )
leg

transl( leg.fkine([0,0,0]) )

leg.plot([0,0,0], 'nobase', 'noshadow', 'notiles')
set(gca, 'Zdir', 'reverse'); view(137,48);

transl( leg.fkine([0.2,0,0]) )

transl( leg.fkine([0,0.2,0]) )

transl( leg.fkine([0,0,0.2]) )

xf = 50; xb = -xf;  y = 50; zu = 20; zd = 50;
path = [xf y zd; xb y zd; xb y zu; xf y zu; xf y zd] * 1e-3;

p = mstraj(path, [], [0, 3, 0.25, 0.5, 0.25]', path(1,:), 0.01, 0);

qcycle = leg.ikine2( SE3(p), 'mask', [1 1 1 0 0 0] );

leg.plot(qcycle, 'loop')

W = 0.1; L = 0.2;

legs(1) = SerialLink(leg, 'name', 'leg1');
legs(2) = SerialLink(leg, 'name', 'leg2', 'base', SE3(-L, 0, 0));
legs(3) = SerialLink(leg, 'name', 'leg3', 'base', SE3(-L, -W, 0) ...
*SE3.Rz(pi));
legs(4) = SerialLink(leg, 'name', 'leg4', 'base', SE3(0, -W, 0) ...
* SE3.Rz(pi));


k = 1;
while 1
    %q = qleg(p,:);
    legs(1).plot( gait(qcycle, k, 0, false) );
    if k == 1, hold on; end
    legs(2).plot( gait(qcycle, k, 100, false) );
    legs(3).plot( gait(qcycle, k, 200, true) );
    legs(4).plot( gait(qcycle, k, 300, true) );
    drawnow
    k = k+1;
end