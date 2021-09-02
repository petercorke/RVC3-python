##  RVC2: Chapter 9 - Dynamics and Control
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

# 9.1 Independent joint control

# %% 9.1.3  Effect of link mass

twolink = models.DH.TwoLink(symbolic=True)

q1, q1d, q1dd, q2, q2d, q2dd = sym.symbol('q1 q1d q1dd q2 q2d q2dd')
tau = twolink.rne_python([q1, q2], [q1d, q2d], [q1dd, q2dd])
print(tau[0])

# %% 9.1.5  Modeling the robot joint
puma = models.DH.Puma560()

tf = puma.jointdynamics(puma.qn);

tf[1]

# %% 9.1.6  Velocity control loop
# vloop_test

# sim('vloop_test')

# %% 9.1.7  Position control loop
# ploop_test

# %% 9.2  Rigid-body equations of motion
puma = models.DH.Puma560()

zero = [0, 0, 0, 0, 0, 0]
Q = puma.rne(puma.qn, zero, zero)

Q = puma.rne(puma.qn, zero, zero, gravity=[0, 0, 0])

traj = jtraj(puma.qz, puma.qr, 10)
Q = puma.rne(traj.q, np.zeros(traj.q.shape), np.zeros(traj.q.shape))
Q.shape

# Q(5,:)

puma.rne(puma.qn, [1, 0, 0, 0, 0, 0], zero, gravity=[0, 0, 0])

puma.links[1].dyn()

# %% 9.2.1  Gravity term
gravload = puma.gravload(puma.qn)

puma.gravity = puma.gravity / 6;

puma.gravload(puma.qn)

puma.base = SE3.Rx(pi);
puma.gravload(puma.qn)

Q = puma.gravload(puma.qs)

Q = puma.gravload(puma.qr)

N = 100
(Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
g1 = np.zeros((N,N))
g2 = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        g = puma.gravload(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
        g1[i,j] = g[1]  # shoulder gravity load
        g2[i,j] = g[2]  # elbow gravity load
plt.axes(projection="3d").plot_surface(Q2, Q3, g1)
plt.pause(1)
plt.axes(projection="3d").plot_surface(Q2, Q3, g2)
plt.pause(1)
# %% 9.2.2  Inertia matrix
# M = puma.inertia(qn)

(Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
M00 = np.zeros((N,N))
M01 = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        M = puma.inertia(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
        M00[i,j] = M[0,0]
        M01[i,j] = M[0,1]
plt.axes(projection="3d").plot_surface(Q2, Q3, M00)
plt.pause(1)
plt.axes(projection="3d").plot_surface(Q2, Q3, M01)
plt.pause(1)

max(M00.flatten()) / min(M00.flatten())

# %% 9.2.3  Coriolis matrix
qd = [0, 0, 1, 0, 0, 0];

C = puma.coriolis(puma.qn, qd)

C @ qd

# %% 9.2.5  Effect of payload
puma.payload(2.5, [0, 0, 0.1]);

M_loaded = puma.inertia(puma.qn);

M_loaded / M

np.seterr(divide='ignore', invalid='ignore')
puma.gravload(puma.qn) / gravload

puma.payload(0)

# %% 9.2.6  Base force

# HACK Q,Wb = puma.rne(puma.qn, zero, zero);
#Wb

sum([link.m for link in puma])

# %% 9.2.7  Dynamic manipulability
J = puma.jacob0(puma.qn);
M = puma.inertia(puma.qn);
Mx = J @ inv(M) @ inv(M).T @ J.T;

Mx = Mx[:3, :3]

plt.clf()
# plot_ellipse( Mx )

e = np.sqrt(np.linalg.eig(Mx)[0])

min(e) / max(e)

puma.manipulability(puma.qn, method='asada')

# %% 9.3  Forward dynamics

# qdd = puma.accel(q, qd, Q);

# sl_ztorque

# clf
# r = sim('sl_ztorque');

# t = r.find('tout');
# q = r.find('yout');

# clf
# puma.plot(q)

# clf
# plot(t, q(:,1:3))

# %% Warning box (page 272)
# p560_nf = puma.nofriction();
# p560_nf = puma.nofriction(coulomb=True, viscous=True);

# %% 9.4  Rigid-body dynamics compensation

# %% 9.4.1  Feed forward control
# mdl_puma560

# sl_fforward

# r = sim('sl_fforward');

# %% 9.4.1  Computed torque control
# mdl_puma560
# sl_ctorque

# r = sim('sl_ctorque');

# t = r.find('tout');

# %% 9.4.3  Operational space control
# sl_opspace

# %% 9.5.1  Series-elastic actuator
# sl_sea