# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from math import pi
np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)

from spatialmath import *
from spatialmath.base import *
from roboticstoolbox import *

# ------------------------------ #


# Manipulator Jacobian


# Jacobian in the World Coordinate Frame

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

# Jacobian in the End-Effector Coordinate Frame

ur5.jacobe(ur5.q1)

# Analytical Jacobian

rotvelxform((0.1, 0.2, 0.3), representation="rpy/xyz")
ur5.jacob0_analytical(ur5.q1, "rpy/xyz");

# Application: Resolved-Rate Motion Control

%run -m RRMC -H
t = out.clock0.t;
q = out.clock0.x;
xplot(t, q[:, :3], stack=True);
Tfk = puma.fkine(q);
xplot(out.clock0.t, Tfk.t, stack=True);
%run -m RRMC2 -H

# Jacobian Condition and Manipulability


# Jacobian Singularities

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

# Velocity Ellipsoid and Manipulability

planar2 = models.ETS.Planar2();
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

# Dealing with Jacobian Singularity


# Dealing with a non-square Jacobian


# Jacobian for Under-Actuated Robot

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

# Jacobian for Over-Actuated Robot

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

# Force Relationships


# Transforming Wrenches to Joint Space

tau = ur5.jacob0(ur5.q1).T @ [0, 20, 0, 0, 0, 0]
tau = ur5.jacob0(ur5.q1).T @ [20, 0,  0, 0, 0, 0]

# Force Ellipsoids


# Numerical Inverse Kinematics


# Advanced Topics


# Manipulability Jacobian

panda = models.ETS.Panda()
panda.jacobm(panda.qr).T

# Computing the Manipulator Jacobian Using Twists


# Manipulability, scaling, and units


# Wrapping Up


# Further Reading


# Exercises

