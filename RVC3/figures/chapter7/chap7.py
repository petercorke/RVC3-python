## CHAPTER 7

from math import pi
from spatialmath import *
from roboticstoolbox import *
from spatialmath import base
import time

## 7.1.1 planar 2D

# R robot

a1 = 1
e = ETS2.r() * ETS2.tx(a1);
e

e.eval(pi / 6)
SE2(pi / 6) * SE2.Tx(a1)

e.teach(block=False)
time.sleep(2)

## RR robot

a1 = 1; a2 = 1;
e = ETS2.r() * ETS2.tx(a1) * ETS2.r() * ETS2.tx(a2);
e
e.eval([30, 40], 'deg').printline()
(SE2(30, unit='deg') * SE2.Tx(a1) * SE2(40, unit='deg') * SE2.Tx(a2)).printline()
e.n
e.joints()
e.structure

e[1].eta
e[1].T()

## RP robot

e = ETS2.r() * ETS2.tx(qlim=[1,2])
e.structure

## 3D robot
a1 = 1; a2 = 1;
e = ETS.rz() * ETS.ry() \
      * ETS.tz(a1) * ETS.ry() * ETS.tz(a2) \
      * ETS.rz() * ETS.ry() * ETS.rz();
e

e.n
e.structure
e.eval((0,)*6)


## rigid body tree

link1 = ELink2(ETS2.r(), name='link1')
link2 = ELink2(ETS2.tx(1) * ETS2.r(), name='link2', parent=link1)
link3 = ELink2(ETS2.tx(1), name='ee_1', parent=link2)

twolink = ERobot2([link1, link2, link3], name='my first robot')

twolink.fkine([30, 40], 'deg').printline()

twolink.plot([30, 40], 'deg')
q = np.array([np.linspace(0, pi, 100), np.linspace(0, -2 * pi, 100)]).T
twolink.plot(q)

link2.parent
link2.children

link2.jindex
link2.isrevolute
link2.isprismatic
link2.qlim

link1.A(pi / 6)

link1.ets()
twolink.fkine([30, 40], unit='deg')

## 3D RBT

a1 = 1; a2 = 1;
robot6 = ERobot(ETS.rz() * ETS.ry() * ETS.tz(a1) * ETS.ry() * ETS.tz(a2) \
                * ETS.rz() * ETS.ry() * ETS.rz())

models.list(mtype='ETS')

panda = models.ETS.Panda()

panda.fkine(panda.qr).printline()
panda.plot(panda.qr, backend='pyplot')

panda.plot(panda.qr, backend='swift')
# tools

panda.base = SE3(0, 0, 3) * SE3.Rx(pi) # robot is 3m up and hanging down
panda.tool = SE3(0, 0, 0.15) # tool is 150mm long in z-direction


# branched robots


robot = ERobot2([
    ELink2(ETS2.r(), name='link1'),
    ELink2(ETS2.tx(1.2) * ETS2.ty(-0.5) * ETS2.r(), name='link2', parent='link1'),
    ELink2(ETS2.tx(1), name='ee_1', parent='link2'),
    ELink2(ETS2.tx(0.6) * ETS2.ty(0.5) * ETS2.r(), name='link3', parent='link1'),
    ELink2(ETS2.tx(1), name='ee_2', parent='link3')
])
print(robot)


robot['link1'].children

# robot.teach()
# robot.plot([0.3, 0.4, -0.6])
robot.fkine([0.3, 0.4, -0.6], end='ee_1').printline()
robot.fkine([0.3, 0.4, -0.6], end='ee_2').printline()
robot.fkine([0.3, 0.4, -0.6], end='ee_1', start='ee_2').printline()

# URDF

urdf = ERobot.URDF_read("ur_description/urdf/ur5_joint_limited_robot.urdf.xacro")

ur5 = models.URDF.UR5()
ur5.plot()
ur5.dynamics()

yumi = models.URDF.YuMi()
q = [0] * 18
q[1] = -0.3
q[10] = -0.5
be = yumi.plot(q)
be.step()

# ## 7.1.2.1 DH params
# L = Revolute('a', 1)

# L.A(0.5)

# L.type

# L.a

# L.offset = 0.5;
# L.A(0)

# robot = SerialLink( [ Revolute('a', 1) Revolute('a', 1) ], ...
# 'name', 'my robot')

# robot.fkine([30 40], 'deg')

# models

# mdl_irb140

# robot.edit

# ## 7.1.2.2 POE

# a1 = 1; a2 = 1;
# TE0 = SE2(a1+a2, 0, 0);

# S1 = Twist( 'R', [0 0] );
# S2 = Twist( 'R', [a1 0] );

# #BUG TE = S1.T(30, 'deg') * S2.T(40, 'deg') *TE0


# ## 7.1.2.3 6-axis industrial

# mdl_puma560

# p560

# TE = p560.fkine(qz)

# p560.tool = SE3(0, 0, 0.2);

# p560.fkine(qz)

# p560.base = SE3(0, 0, 30*0.0254);
# p560.fkine(qz)

# p560.base = SE3(0,0,3) * SE3.Rx(pi);
# p560.fkine(qz)

# q=jtraj(qz, qr, 8);
# q

# T = p560.fkine(q);

# about(T)

# T(4)

## 7.2.1.1 inv kine closed form



# ## 7.2.2 3D inv kine

puma = models.DH.Puma560();
puma.qn
T = puma.fkine(puma.qn)
T.printline()

sol = puma.ikine_a(T)
sol.q
puma.fkine(sol.q).printline()


sol = puma.ikine_a(T, 'ru')
sol.q

puma.ikine_a(SE3(3, 0, 0))


q = [0, pi/4, pi, 0.1, 0, 0.2];
puma.ikine_a(puma.fkine(q), 'ru').q

q[3] + q[5]

## 7.2.2.2 numerical 3D

T = puma.fkine(puma.qn)
T.printline()
sol = puma.ikine_LM(T);
sol.q
puma.qn

puma.fkine(sol.q).printline()

puma.plot(sol.q)


puma.ikine_LM(T, q0=[0, 0, 3, 0, 0, 0])

## 7.2.2.3
cobra = models.DH.Cobra600()

TE = SE3(0.4, -0.3, 0.2) * SE3.RPY(30, 0, 170, unit='deg', order='xyz');
sol = cobra.ikine_LM(TE)
sol = cobra.ikine_LM(TE, mask=[1, 1, 1, 0, 0, 1])
cobra.fkine(sol.q).printline('rpy/xyz')

TE.plot(color='r')
cobra.fkine(sol.q).plot(color='b')


## 7.2.2.4 redundant

panda = models.DH.Panda()

TE = SE3(0.7, 0.2, 0.1) * SE3.Ry(pi);

sol = panda.ikine_LM(TE)

panda.fkine(sol.q).printline('angvec')

## 7.3.1 trajectories

TE1 = SE3(0.4, -0.2, 0.6) * SE3.Rx(pi);
TE2 = SE3(0.4, 0.2, 0.6) * SE3.Rx(pi/2);
t = np.arange(0, 2, 0.02);

sol1 = puma.ikine_a(TE1, 'ru');
sol2 = puma.ikine_a(TE2, 'ru');


traj = mtraj(tpoly, sol1.q, sol2.q, t);

# traj = mtraj(lspb, sol1.q, sol2.q, t);
traj.q.shape

traj = jtraj(sol1.q, sol2.q, t)


# traj = puma.jtraj(T1, T2, t)

puma.plot(traj.q)


qplot(t, q);

T = puma.fkine(traj.q);
p = T.t

p.shape

plt.plot(p[:,0], p[:,1])

plot(t, T.torpy('xyz'))

## 7.3.2 cartesian motion

Ts = ctraj(TE1, TE2, t);

qplot(t, Ts.t);
qplot(t, Ts.rpy('xyz'), label=[]);

qc = p560.ikine6s(Ts);

## 7.3.3 kinematics in simulink

%run models/jointspace

## 7.3.4 motion through singularity

TE1 = SE3(0.5, -0.3, 1.12) * SE3.Ry(pi/2);
TE2 = SE3(0.5, 0.3, 1.12) * SE3.Ry(pi/2);
t = np.arange(0, 2, 0.02);

Ts = ctraj(TE1, TE2, t);

sol = puma.ikine_a(Ts, 'lu');
qplot(t, sol.q)

m = puma.manipulability(sol.q);

## 7.3.5 config change

T = SE3(0.4, 0.2, 0.6) * SE3.Rx(pi);

sol_r = puma.ikine_a(T, 'ru');
sol_l = puma.ikine_a(T, 'lu');

traj = jtraj(sol_r.q, sol_l.q, t);

puma.plot(traj.q)

# ## 7.4.2 determining DH params


# s = 'Tz(L1) Rz(q1) Ry(q2) Ty(L2) Tz(L3) Ry(q3) Tx(L4) Ty(L5) Tz(L6) Rz(q4) Ry(q5) Rz(q6)'

# dh = DHFactor(s);

# dh

# cmd = dh.command('puma')

# robot = eval(cmd)

# ## 7.4.3 MDH

# L1 = RevoluteMDH('d', 1)

# ## 7.5.1 writing

# load hershey

# B = hershey{'B'}

# B.stroke

# path = [ 0.25*B.stroke; zeros(1,numcols(B.stroke))];
# k = find(isnan(path(1,:)))
# path(:,k) = path(:,k-1); path(3,k) = 0.2;

# traj = mstraj(path(:,2:end)', [0.5 0.5 0.5], [], path(:,1)', ...
# 0.02, 0.2);

# about(traj)

# numrows(traj) * 0.02

# plot3(traj(:,1), traj(:,2), traj(:,3))

# Tp = SE3(0.6, 0, 0) * SE3(traj) * SE3.oa( [0 1 0], [0 0 -1]);

# q = p560.ikine6s(Tp);

# p560.plot(q)

# ## 7.1.2 3D arms

# l1 = 0.672
# l2 = -0.2337
# l3 = 0.4318
# l4 = 0.0203
# l5 = 0.0837
# l6 = 0.4318

# e = ETS.tz(l1) * ETS.rz() * ETS.ty(l2) * ETS.ry() \
#     * ETS.tz(l3) * ETS.tx(l4) * ETS.ty(l5) * ETS.ry() \
#     * ETS.tz(l6) * ETS.rz() * ETS.ry() * ETS.rz()
# robot = ERobot(e)
# print(robot)
# # robot.plot((0,)*6, backend='pyplot', block=True)
# robot.teach()
# # #BUG E3.fkine([0 0 0 0 0 0])

# ## 7.5.2 walking

# Collision detection


# PoE Robot

puma = models.DH.Puma560()
robot.plot(robot.qz, backend='pyplot')

robot = models.DH.IRB140()
S, T0 = robot.twists()
S 
S.exp(robot.qr).prod() * T0

robot.plot(robot.qz)

tw = S.exp(robot.qr)


lines = S.line()
lines.plot('k:')

