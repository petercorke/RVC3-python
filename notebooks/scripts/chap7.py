# # 7.1 Forward Kinematics
#

# ## 7.1.1 Forward kinematics from a pose graph
#

# ### 7.1.1.1 2-Dimensional (Planar) Robotic Arms
#

a1 = 1;
e = ET2.R() * ET2.tx(a1);

len(e)

e

e.fkine(pi / 6)

SE2.Rot(pi / 6) * SE2.Tx(a1)

e.teach()

a1 = 1; a2 = 1;
e = ET2.R() * ET2.tx(a1) * ET2.R() * ET2.tx(a2);

e

e.fkine(np.deg2rad([30, 40])).printline()

T = SE2.Rot(np.deg2rad(30)) * SE2.Tx(a1) * SE2.Rot(np.deg2rad(40)) * SE2.Tx(a2);
T.printline()

e.n
e.joints()

e.structure

e.plot(np.deg2rad([30, 40]));

e[1]

e[1].eta
e[1].A()

e = ET2.R() * ET2.tx(qlim=[1,2])

e.structure

# ### 7.1.1.2 3-Dimensional Robotic Arms
#

a1 = 1; a2 = 1;
e = ET.Rz() * ET.Ry() \ 
     * ET.tz(a1) * ET.Ry() * ET.tz(a2) \
     * ET.Rz() * ET.Ry() * ET.Rz();

e.n
e.structure

e.fkine(np.zeros((6,)))

# ## 7.1.2 Forward kinematics as a chain of robot links
#

# ### 7.1.2.1 2-Dimensional (Planar) case
#

link1 = Link2(ET2.R(), name="link1");
link2 = Link2(ET2.tx(1) * ET2.R(), name="link2", parent=link1);
link3 = Link2(ET2.tx(1), name="link3", parent=link2);

robot = ERobot2([link1, link2, link3], name="my robot")

robot.fkine(np.deg2rad([30, 40])).printline()

robot.plot(np.deg2rad([30, 40]));

q = np.array([np.linspace(0, pi, 100), np.linspace(0, -2 * pi, 100)]).T;
q.shape
robot.plot(q);

robot[1]

robot["link2"]

robot.ee_links

link2.parent

link2.children

link2.jindex

link2.isrevolute
link2.isprismatic

print(link2.qlim)

link2.A(pi / 6)

link2.ets

# ### 7.1.2.2 3-Dimensional case
#

a1 = 1; a2 = 1;
robot6 = ERobot(ET.Rz() * ET.Ry() * ET.tz(a1) * ET.Ry() \
                * ET.tz(a2) * ET.Rz() * ET.Ry() * ET.Rz())

models.list(type="ETS")

panda = models.ETS.Panda()

panda.qr

panda.addconfiguration("foo", [1, 2, 3, 4, 5, 6, 7]) 

panda.configs["foo"];
panda.configs["qz"];

panda.fkine(panda.qr).printline()

panda.plot(panda.qr);

T = panda.fkine_all(panda.qr);
len(T)

T[1].printline()

# ### 7.1.2.3 Tools and bases
#

panda.base = SE3.Tz(3) * SE3.Rx(pi); # robot is 3m up and hanging down
panda.tool = SE3.Tz(0.15); # tool is 150mm long in z-direction

panda.fkine(panda.qr, tool=SE3.Trans(0.05, 0.02, 0.20) * SE3.Rz(np.deg2rad(45)));

# ## 7.1.3 Branched robots
#

# ### 7.1.3.1 2D (Planar) Branched robots
#

robot = ERobot2([
  Link2(ET2.R(), name="link1"),
  Link2(ET2.tx(1) * ET2.tx(1.2) * ET2.ty(-0.5) * ET2.R(), name="link2", parent="link1"),
  Link2(ET2.tx(1), name="ee_1", parent="link2"),
  Link2(ET2.tx(1) * ET2.tx(0.6) * ET2.ty(0.5) * ET2.R(), name="link3", parent="link1"),
  Link2(ET2.tx(1), name="ee_2", parent="link3") ], name="branched");

robot["link1"].children

robot

robot.showgraph()

robot.teach()
robot.plot([0.3, 0.4, -0.6]);

robot.fkine([0.3, 0.4, -0.6], end="ee_2")

robot.fkine([0.3, 0.4, -0.6], end="ee_2", start="ee_1")

# ## 7.1.4 Unified Robot Description Format (URDF)
#

urdf, *_ = ERobot.URDF_read("ur_description/urdf/ur5_joint_limited_robot.urdf.xacro")
urdf

ur5 = models.URDF.UR5()

ur5.showgraph()

ur5.grippers

ur5.plot(ur5.qr);

ur5.dynamics()

yumi = models.URDF.YuMi()

yumi.showgraph(ets="brief")

yumi.grippers

yumi.plot(yumi.q1);

models.list(type="URDF")


pr2 = models.URDF.PR2()

pr2
pr2.showgraph()
pr2.plot(pr2.qz)

# ## 7.1.5 Denavit-Hartenberg Parameters
#

link = RevoluteDH(a=1)

link.A(0.5)

models.list(type="DH")


irb140 = models.DH.IRB140();

irb140

irb140.fkine(irb140.qr).printline("rpy/xyz")

irb140.plot(irb140.qr);

irb140.teach()

irb140.ets()

# # 7.2 Inverse Kinematics
#

# ## 7.2.1 2-Dimensional (Planar) Robotic Arms
#

# ### 7.2.1.1 Closed-Form Solution
#

import sympy
a1, a2 = sympy.symbols("a1 a2")
e = ET2.R() * ET2.tx(a1) * ET2.R() * ET2.tx(a2);

q0, q1 = sympy.symbols("q0 q1")

TE = e.fkine([q0, q1])
x_fk, y_fk = TE.t;

x, y = sympy.symbols("x y")

eq1 = (x_fk**2 + y_fk**2 - x**2 - y**2).trigsimp()  

q1_sol = sympy.solve(eq1, q1) 
eq0 = tuple(map(sympy.expand_trig, [x_fk - x, y_fk - y]))
q0_sol = sympy.solve(eq0, [sympy.sin(q0), sympy.cos(q0)]);

sympy.atan2(q0_sol[sympy.sin(q0)], q0_sol[sympy.cos(q0)]).simplify()

# ### 7.2.1.2 Numerical Solution
#

e = ET2.R() * ET2.tx(1) * ET2.R() * ET2.tx(1);

pstar = np.array([0.6, 0.7]);  # desired position
E = lambda q: np.linalg.norm(e.fkine(q).t - pstar);

sol = sp.optimize.minimize(E, [0, 0]);

sol.x

e.fkine(sol.x).printline()

# ## 7.2.2 3-Dimensional Robotic Arms
#

# ### 7.2.2.1 Closed-Form Solution
#

puma = models.DH.Puma560();

puma.qn

T = puma.fkine(puma.qn);
T.printline()

sol = puma.ikine_a(T)

sol.q

puma.fkine(sol.q).printline()

sol = puma.ikine_a(T, "r");
sol.q

puma.ikine_a(SE3.Tx(3))

q = [0, pi/4, pi, 0.1, 0, 0.2];

puma.ikine_a(puma.fkine(q), "ru").q

# ### 7.2.2.2 Numerical Solution
#

T = puma.fkine(puma.qn);
T.printline("rpy/xyz")
sol = puma.ikine_LM(T)

puma.qn

puma.fkine(sol.q).printline("rpy/xyz")

puma.plot(sol.q);

puma.ikine_LM(T, q0=[0, 0, 3, 0, 0, 0])

# ## 7.2.3 Underactuated Manipulator
#

cobra = models.DH.Cobra600()

TE = SE3.Trans(0.4, -0.3, 0.2) * SE3.RPY(np.deg2rad([30, 0, 170]), order="xyz");

sol = cobra.ikine_LM(TE)

sol = cobra.ikine_LM(TE, mask=[1, 1, 1, 0, 0, 1])

cobra.fkine(sol.q).printline("rpy/xyz")

TE.plot(color="r");
cobra.fkine(sol.q).plot(color="b");

# ## 7.2.4 Overactuated (Redundant) Manipulator
#

panda = models.ETS.Panda();

TE = SE3.Trans(0.7, 0.2, 0.1) * SE3.OA((0, 1, 0), (0, 0, -1));

sol = panda.ikine_LM(TE)

panda.fkine(sol.q).printline("angvec")

# # 7.3 Trajectories
#

# ## 7.3.1 Joint-Space Motion
#

TE1 = SE3.Trans(0.4, -0.2, 0) * SE3.Rx(3);
TE2 = SE3.Trans(0.4, 0.2, 0) * SE3.Rx(1);

sol1 = puma.ikine_a(TE1, "ru");
sol2 = puma.ikine_a(TE2, "ru");

t = np.arange(0, 2, 0.02);

traj = mtraj(quintic, sol1.q, sol2.q, t);

traj = mtraj(trapezoidal, sol1.q, sol2.q, t);

traj.q.shape

traj = jtraj(sol1.q, sol2.q, t)

puma.plot(traj.q);

xplot(t, traj.q);

T = puma.fkine(traj.q);
len(T)

p = T.t; 
p.shape

xplot(t, T.t, labels="x y z");

xplot(t, T.rpy("xyz"), labels="roll pitch yaw");

# ## 7.3.2 Cartesian Motion
#

Ts = ctraj(TE1, TE2, t);

xplot(t, Ts.t, labels="x y z");

xplot(t, Ts.rpy("xyz"), labels="roll pitch yaw");

qc = puma.ikine_a(Ts);

# ## 7.3.3 Kinematics in a block diagram
#

%run -m jointspace -H

# ## 7.3.4 Motion through a Singularity
#

TE1 = SE3.Trans(0.5, -0.3, 1.12) * SE3.OA((0, 1, 0), (1, 0, 0));
TE2 = SE3.Trans(0.5, 0.3, 1.12) * SE3.OA((0, 1, 0), (1, 0, 0)); 

Ts = ctraj(TE1, TE2, t);

sol = puma.ikine_a(Ts, "lu");

xplot(t, sol.q, unwrap=True);

m = puma.manipulability(sol.q);

# ## 7.3.5 Configuration Change
#

TE = SE3.Trans(0.4, 0.2, 0.6) * SE3.Rx(pi);

sol_r = puma.ikine_a(TE, "ru");
sol_l = puma.ikine_a(TE, "lu");

traj = jtraj(sol_r.q, sol_l.q, t);

puma.plot(traj.q);

# # 7.4 Applications
#

# ## 7.4.1 Writing on a surface
#

font = rtb_load_jsonfile("data/hershey.json");

letter = font["B"]

lift = 0.1; # height to raise the pen
scale = 0.25;
via = np.empty((0, 3));
for stroke in letter["strokes"]:
  xyz = np.array(stroke) * scale # convert stroke to nx2 array
  xyz = np.pad(xyz, ((0, 0), (0, 1))) # add third column, z=0
  via = np.vstack((via, xyz))  # append rows to via points
  via = np.vstack((via, np.hstack([xyz[-1,:2], lift]))) # lift pen

xyz_traj = mstraj(via, qdmax=[0.5, 0.5, 0.5], q0=[0, 0, lift], 
                  dt=0.02, tacc=0.2).q;

len(xyz_traj)

len(xyz_traj) * 0.02

fig = plt.figure(); ax = fig.add_subplot(111, projection="3d");
plt.plot(xyz_traj[:,0], xyz_traj[:,1], xyz_traj[:,2]);

T_pen = SE3.Trans(0.6, 0, 0.7) * SE3.Trans(xyz_traj) * SE3.OA( [0, 1, 0], [0, 0, -1]);

puma = models.DH.Puma560();
sol = puma.ikine_a(T_pen, "lu");

puma.plot(sol.q);

%run -m writing

# ## 7.4.2 A 4-Legged Walking robot
#

mm = 0.001;  # millimeters
L1 = 100 * mm;
L2 = 100 * mm;

leg = ERobot(ET.Rz() * ET.Rx() * ET.ty(-L1) * ET.Rx() * ET.tz(-L2))

leg.fkine([0,0,0]).t

leg.plot([0, 0, 0]);

# ### 7.4.2.1 Motion of One Leg
#

xf = 50; xb = -xf;  y = -50; zu = -20; zd = -50;
via = np.array([
  [xf, y, zd],
  [xb, y, zd],
  [xb, y, zu],
  [xf, y, zu],
  [xf, y, zd]]) * mm;

x = mstraj(via, tsegment=[3, 0.25, 0.5, 0.25], dt=0.01, tacc=0.1).q

sol = leg.ikine_LM(SE3.Trans(x), mask=[1, 1, 1, 0, 0, 0]);

leg.plot(sol.q);

# ### 7.4.2.2 Motion of Four Legs
#

W = 100 * mm; L = 200 * mm;

Tflip = SE3.Rz(pi);
legs = [
  ERobot(leg, name="leg0", base=SE3.Trans( L/2,  W/2, 0)),
  ERobot(leg, name="leg1", base=SE3.Trans(-L/2,  W/2, 0)),
  ERobot(leg, name="leg2", base=SE3.Trans( L/2, -W/2, 0) * Tflip),
  ERobot(leg, name="leg3", base=SE3.Trans(-L/2, -W/2, 0) * Tflip)];

for i in range(4000):
  legs[0].q = gait(qcycle, i, 0, False)
  legs[1].q = gait(qcycle, i, 100, False)
  legs[2].q = gait(qcycle, i, 200, True)
  legs[3].q = gait(qcycle, i, 300, True)
env.step(dt=0.02)  # render the graphics

def gait(cycle, k, phi, flip):
  k = (k + phi) % cycle.shape[0]  # modulo addition
  q = cycle[k, :]
  if flip:
    q[0] = -q[0]  # for right-side legs
  return q

%run -m walking

# # 7.5 Advanced Topics
#

# ## 7.5.1 Zero-angle configuration
#

# ## 7.5.2 Creating the Kinematic Model for a Robot
#

L1 = 0.672; L2 = -0.2337; L3 = 0.4318;
L4 = 0.0203; L5 = 0.0837; L6 = 0.4318;

e = ET.tz(L1) * ET.Rz() * ET.ty(L2) * ET.Ry() \
   * ET.tz(L3) * ET.tx(L4) * ET.ty(L5) * ET.Ry() \
   * ET.tz(L6) * ET.Rz() * ET.Ry() * ET.Rz();

robot = ERobot(e)

# ## 7.5.3 Modified Denavit-Hartenberg Parameters
#

L1 = RevoluteMDH(d=1)

# ## 7.5.4 Products of exponentials
#

a1 = 1; a2 = 1;
TE0 = SE2(a1 + a2, 0, 0);

S0 = Twist2.UnitRevolute([0, 0]);
S1 = Twist2.UnitRevolute([a1, 0]);

TE = S0.exp(np.deg2rad(30)) * S1.exp(np.deg2rad(40)) * TE0

irb140 = models.DH.IRB140();
S, TE0 = irb140.twists()
S

T = S.exp(irb140.qr).prod() * TE0

irb140.plot(irb140.qz);

lines = S.line()
lines.plot("k:")

link1 = PoERevolute([0, 0, 1], [0, 0, 0]);  # rotate about z-axis, through (0,0,0)
link2 = PoERevolute([0, 0, 1], [1, 0, 0]);  # rotate about z-axis, through (1,0,0)
TE0 = SE3.Tx(2);  # end-effector pose when q=[0,0]

robot = PoERobot([link1, link2], TE0);

robot.fkine([0, 0]).printline()

# ## 7.5.5 Collision detection
#

panda = models.URDF.Panda();

from spatialgeometry import Cuboid
box = Cuboid([1, 1, 1], pose=SE3.Tx(1.1));

panda.iscollided(panda.qr, box)

box.T = SE3.Tx(1)
panda.iscollided(panda.qr, box)

# plot robot and get reference to graphics environment
env = panda.plot(panda.qr, backend="swift");  
env.add(box);  # add box to graphics
env.step()     # update the graphics

env.step()

# # 7.6 Wrapping Up
#

# ## 7.6.1 Further Reading
#

# ### 7.6.1.1 Historical
#

# ## 7.6.2 Exercises
#

