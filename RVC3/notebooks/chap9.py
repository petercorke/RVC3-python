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


# Independent Joint Control


# Actuators


# Friction


# Effect of the Link Mass

import sympy
a1, a2, r1, r2, m1, m2, g = sympy.symbols("a1 a2 r1 r2 m1 m2 g")
link1 = Link(ET.Ry(flip=True), m=m1, r=[r1, 0, 0], name="link0")
link2 = Link(ET.tx(a1) * ET.Ry(flip=True), m=m2, r=[r2, 0, 0], name="link1")
robot = ERobot([link1, link2])
robot.dynamics()
q = sympy.symbols("q:2")
qd = sympy.symbols("qd:2")
qdd = sympy.symbols("qdd:2")
tau = robot.rne(q, qd, qdd, gravity=[0, 0, g], symbolic=True);

# Gearbox


# Modeling the Robot Joint

puma = models.DH.Puma560();  # load model of PUMA560 with dynamic parameters
tf = puma.jointdynamics(puma.qn);
tf[1]

# Velocity Control Loop


# Position Control Loop


# Independent Joint Control Summary


# Rigid-Body Equations of Motion

puma = models.DH.Puma560();
zero = np.zeros((6,));
Q = puma.rne(puma.qn, zero, zero)
Q = puma.rne(puma.qn, zero, zero, gravity=[0, 0, 0])
traj = jtraj(puma.qz, puma.qr, 10);
Q = puma.rne(traj.q, traj.qd, traj.qdd);
Q.shape
Q[5, :]
puma.rne(puma.qn, [1, 0, 0, 0, 0, 0], zero, gravity=[0, 0, 0])
 print(puma[1].dyn())

# Gravity Term

Q = puma.gravload(puma.qn)
puma.gravity
puma.gravity /= 6
puma.gravload(puma.qn)
puma.base = SE3.Rx(pi);
puma.gravload(puma.qn)
puma = models.DH.Puma560();
Q = puma.gravload(puma.qs)
Q = puma.gravload(puma.qr)
N = 100;
Q1, Q2 = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N));
G1, G2 = np.zeros((N,N)), np.zeros((N,N));
for i in range(N):
  for j in range(N):
    g = puma.gravload(np.array([0, Q1[i,j], Q2[i,j], 0, 0, 0]))
    G1[i, j] = g[1]  # shoulder gravity load
    G2[i, j] = g[2]  # elbow gravity load
plt.axes(projection="3d").plot_surface(Q1, Q2, G1);

# Inertia Matrix

M = puma.inertia(puma.qn)
N = 100;
Q1, Q2 = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N));
M00, M01, M11 = np.zeros((N,N)), np.zeros((N,N)), np.zeros((N,N));
for i in range(N):
  for j in range(N):
    M = puma.inertia(np.array([0, Q1[i,j], Q2[i,j], 0, 0, 0]))
    M00[i, j] = M[0, 0]
    M01[i, j] = M[0, 1]
    M11[i, j] = M[1, 1]
plt.axes(projection="3d").plot_surface(Q1, Q2, M00);
M00.max() / M00.min()

# Friction

puma.friction([1, 0, 0, 0, 0, 0])

# Coriolis and Centripetal Matrix

qd = [0, 0, 1, 0, 0, 0];
C = puma.coriolis(puma.qn, qd)
C @ qd

# Effect of Payload

G = puma.gravload(puma.qn);
M = puma.inertia(puma.qn);
puma.payload(2.5, [0, 0, 0.1]);
M_loaded = puma.inertia(puma.qn);
M_loaded / np.where(M < 1e-6, np.nan, M)
puma.gravload(puma.qn) / np.where(G < 1e-6, np.nan, G)
puma.payload(0)

# Base Wrench

Q, wb = puma.rne(puma.qn, zero, zero, base_wrench=True);
wb
sum([link.m for link in puma]) * puma.gravity[2]

# Dynamic Manipulability

Jt = puma.jacob0(puma.qn, half="trans");  # first 3 rows
M = puma.inertia(puma.qn);
E = (Jt @ np.linalg.inv(M) @ np.linalg.inv(M).T @ Jt.T);
plot_ellipsoid(E);
e, _ = np.linalg.eig(E)
radii = 1 / np.sqrt(e)
radii.min() / radii.max()
puma.manipulability(puma.qn, method="asada")

# Forward Dynamics

puma_nf = puma.nofriction();

# Rigid-Body Dynamics Compensation


# Feedforward Control


# Computed-Torque Control


# Task-Space Dynamics and Control

xd = [0, 0.1, 0, 0, 0, 0];
qd = np.linalg.inv(puma.jacob0_analytical(puma.qn, "eul")) @ xd;
Cx = puma.coriolis_x(puma.qn, qd, representation="eul");
Cx @ xd
Mx = puma.inertia_x(puma.qn, representation="eul")
np.linalg.inv(Mx) @ [10, 0, 0, 0, 0, 0]

# Applications


# Operational Space Control


# Series-Elastic Actuator (SEA)


# Exercises

