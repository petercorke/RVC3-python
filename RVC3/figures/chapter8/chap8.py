#! /usr/bin/env python3
##  RVC3: Chapter 8 - Velocity Relationships

import time
import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from math import pi, sqrt
import scipy as sp
import sympy

from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE3, SO2, SO3, UnitQuaternion
from roboticstoolbox import *
from spatialmath.base import symbol


#np.set_printoptions(linewidth=120, formatter={'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})


# %% 8.1  Manipulator Jacobian
# planar2 = models.DH.Planar2(symbolic=True)
# q1, q2 = sym.symbol('q1 q2')

# Te = planar2.fkine([q1, q2])
# print(Te)

# p = Te.t[:2]
# print(p)

# J = sympy.Matrix(p).jacobian([q1, q2])
# J.simplify()
# sympy.printing.pretty_print(J)


q1, q2 = sym.symbol('q1 q2')
a1, a2 = sym.symbol('a1 a2')

e = ETS2.r() * ETS2.tx(a1) * ETS2.r() * ETS2.tx(a2)
print(e)

print(e[0].T(q1) @ e[1].T() @ e[2].T(q2) @ e[3].T())
print(e[0].T(q1) @ e[1].T() )

Te = e.eval([q1, q2])
print(Te)

p = sympy.Matrix(Te.t)
print(p)

J = p.jacobian([q1, q2])
J.simplify()
sympy.printing.pretty_print(J)


puma = models.DH.Puma560()
J = puma.jacob0(puma.qn)
print(J)

# puma.teach(puma.qn)

# %% 8.1.1  Jacobian in end-effector coordinate frame
puma.jacobe(puma.qn)

# %% 8.1.2  Analytical Jacobian
rpy2jac(0.1, 0.2, 0.3, order='xyz')

puma.jacob0(puma.qn, analytical='eul');

#  8.2 Jacobian condition and manipulability

#  %%8.2.1  Jacobian singularities
J = puma.jacob0(puma.qr)

np.linalg.det(J)

np.linalg.matrix_rank(J)


jsingu(J)

qns = puma.qr.copy(); qns[4] = np.deg2rad(5)
print(qns)

J = puma.jacob0(qns);

qd = np.linalg.inv(J) @ [0, 0, 0.1, 0, 0, 0];
qd

np.linalg.det(J)

np.linalg.cond(J)
qd = np.linalg.inv(J) @ [0, 0, 0, 0, 0.2, 0];
qd

# %% 8.2.2  Manipulability
# clf
planar2 = models.DH.Planar2()
print(planar2)

e = planar2.vellipse([30, 40], unit='deg')
e.plot2()

planar2.teach2([0, 0], vellipse=True)

# , 'callback', @vellipse, 'view', 'top')

J = puma.jacob0(qns);
J = J[:3, :3]

A = J @ J.T

e, x = np.linalg.eig(A)
print(e)
print(x)

plot_ellipsoid(J @ J.T)
plt.show(block=True)

# clf
e = puma.vellipse(qns, 'trans')
e.plot()

# clf
# puma.vellipse(qns, 'rot')

m = puma.manipulability(puma.qr)

puma.manipulability(puma.qr, axes='both')

puma.manipulability(puma.qn, axes='both')

puma.jacobm(puma.qn)

# %% 8.3  Resolved-rate motion control
# sl_rrmc

# clf
# r = sim('sl_rrmc');

# t = r.find('tout');
# q = r.find('yout');

# T = puma.fkine(q);
# xyz = transl(T);

# mplot(t, xyz(:,1:3))
# pause(1)
# clf
# mplot(t, q(:,1:3))

# sl_rrmc2
# clf
# sim('sl_rrmc2');

#  8.4  Under- and over- actuated manipulators

# ## 8.4.1 Jacobian for under actuated robot
planar2 = models.ETS.Planar2();

qn = [1, 1]

J = planar2.jacob0(qn)

xd_desired = [0.1, 0, 0];
qd = np.linalg.pinv(J) @ xd_desired

xd = J @ qd

np.linalg.norm(xd_desired - J @ qd)

Jxy = J[:2,:];
qd = np.linalg.inv(Jxy) @ xd_desired[:2]

xd = J @ qd

np.linalg.norm(xd_desired - J @ qd)

# # 8.4.2  Jacobian for over-actuated robot

panda = models.DH.Panda()
Te = SE3(0.3, -0.1, 0.4) * SE3.Rx(pi);
sol = panda.ikine_LM(Te)
print(sol)

J = panda.jacob0(sol.q);
J.shape

xd = [0.2, 0.2, 0.2, 0, 0, 0];
qd = np.linalg.pinv(J) @ xd

(J @ qd).T

np.linalg.matrix_rank(J)

N = sp.linalg.null_space(J)

np.linalg.norm(J @ N[:,0])

qd_null = [0, 0, 0, 0, 1, 0, 0];

qp = N @ sp.linalg.pinv(N) @ qd_null

np.linalg.norm( J @ qp)

# 8.5 Force relationships

puma = models.DH.Puma560()

# %% 8.5.1 Transforming wrenches into joint space
tau = puma.jacob0(puma.qn).T @ [0, 20, 0, 0, 0, 0]

tau = puma.jacob0(puma.qn).T @ [20, 0, 0, 0, 0, 0]

# # 8.5.2  Force ellipsoids
# clf
planar2.fellipse([30, 40], unit='deg')

planar2.teach(fellipse=True)

# clf
# p2.teach([0 0], 'callback', @(r,q) r.fellipse(q), 'view', 'top')

