# # 8.1 Manipulator Jacobian
#

# ## 8.1.1 Jacobian in the World Coordinate Frame
#

import sympy
a1, a2 = sympy.symbols("a1, a2")
e = ERobot2(ET2.R() * ET2.tx(a1) * ET2.R() * ET2.tx(a2))

q = sympy.symbols("q:2")

TE = e.fkine(q);

p = TE.t

J = sympy.Matrix(p).jacobian(q)
J.shape

ur5 = models.URDF.UR5();
J = ur5.jacob0(ur5.q1)

ur5.teach(ur5.q1)

# ## 8.1.2 Jacobian in the End-Effector Coordinate Frame
#

ur5.jacobe(ur5.q1)

# ## 8.1.3 Analytical Jacobian
#

rotvelxform((0.1, 0.2, 0.3), representation="rpy/xyz")

ur5.jacob0_analytical(ur5.q1, "rpy/xyz");

# # 8.2 Application: Resolved-Rate Motion Control
#

%run -m RRMC -H

t = out.clock0.t;
q = out.clock0.x;

xplot(t, q[:, :3], stack=True);

Tfk = puma.fkine(q);

xplot(out.clock0.t, Tfk.t, stack=True);

%run -m RRMC2 -H

# # 8.3 Jacobian Condition and Manipulability
#

# ## 8.3.1 Jacobian Singularities
#

J = ur5.jacob0(ur5.qz)

np.linalg.det(J)

np.linalg.matrix_rank(J)

jsingu(J)

qns = np.full((6,), np.deg2rad(5))

J = ur5.jacob0(qns);

qd = np.linalg.inv(J) @ [0, 0, 0, 0.1, 0, 0]

np.linalg.det(J)

np.linalg.cond(J)

qd = np.linalg.inv(J) @ [0, 0.1, 0, 0, 0, 0]

# ## 8.3.2 Velocity Ellipsoid and Manipulability
#

planar2 = models.ETS.Planar2();

planar2.teach(np.deg2rad([30, 40]), vellipse=True);

J = ur5.jacob0(ur5.q1);

Jt = J[:3, :];  # first 3 rows

E = np.linalg.inv(Jt @ Jt.T)
plot_ellipsoid(E);

e, _ = np.linalg.eig(E);
radii = 1 / np.sqrt(e)

J = ur5.jacob0(np.full((6,), np.deg2rad(1)));
Jr = J[3:, :];  # last 3 rows
E = np.linalg.inv(Jr @ Jr.T);
plot_ellipsoid(E);

e, x = np.linalg.eig(E);
radii = 1 / np.sqrt(e)

x[:, 0]

ur5.vellipse(qns, "rot");

ur5.manipulability(ur5.q1)

ur5.manipulability(ur5.qz)

ur5.manipulability(ur5.qz, axes="both")

# ## 8.3.3 Dealing with Jacobian Singularity
#

# ## 8.3.4 Dealing with a non-square Jacobian
#

# ### 8.3.4.1 Jacobian for Under-Actuated Robot
#

planar2 = models.ETS.Planar2();
qn = [1, 1];

J = planar2.jacob0(qn)

xd_desired = [0.1, 0.2, 0];

qd = np.linalg.pinv(J) @ xd_desired

J @ qd

np.linalg.norm(xd_desired - J @ qd)

Jxy = J[:2, :];
qd = np.linalg.inv(Jxy) @ xd_desired[:2]

xd = J @ qd

np.linalg.norm(xd_desired - J @ qd)

# ### 8.3.4.2 Jacobian for Overactuated Robot
#

panda = models.ETS.Panda();
TE = SE3.Trans(0.5, 0.2, -0.2) * SE3.Ry(pi);
sol = panda.ikine_LMS(TE);

J = panda.jacob0(sol.q);
J.shape

xd_desired = [0.1, 0.2, 0.3, 0, 0, 0];

qd = np.linalg.pinv(J) @ xd_desired

J @ qd

np.linalg.matrix_rank(J)

N = sp.linalg.null_space(J);
N.shape
N.T

np.linalg.norm( J @ N[:,0])

qd_0 = [0, 0, 0, 0, 1, 0, 0];

qd = N @ np.linalg.pinv(N) @ qd_0

np.linalg.norm(J @ qd)

# # 8.4 Force Relationships
#

# ## 8.4.1 Transforming Wrenches to Joint Space
#

tau = ur5.jacob0(ur5.q1).T @ [0, 20, 0, 0, 0, 0]

tau = ur5.jacob0(ur5.q1).T @ [20, 0,  0, 0, 0, 0]

# ## 8.4.2 Force Ellipsoids
#

planar2.teach(np.deg2rad([30, 40]), fellipse=True);

# # 8.5 Numerical Inverse Kinematics
#

# # 8.6 Advanced Topics
#

# ## 8.6.1 Manipulability Jacobian
#

panda = models.ETS.Panda()
panda.jacobm(panda.qr).T

# ## 8.6.2 Computing the Manipulator Jacobian Using Twists
#

# ## 8.6.3 Manipulability, scaling, and units
#

# # 8.7 Wrapping Up
#

# ## 8.7.1 Further Reading
#

# ## 8.7.2 Exercises
#

