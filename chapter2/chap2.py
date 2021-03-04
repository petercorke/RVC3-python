# %% [markdown]
# # RVC3 chapter 2
#

# %%
import numpy as np
from numpy.core.shape_base import _block_dispatcher
from numpy.linalg import *
import matplotlib.pyplot as plt
from math import pi, sqrt
import scipy as sp
from sympy import simplify
import mpl_toolkits.mplot3d as m3d
from spatialmath.base import *
from spatialmath.base import sym
from spatialmath import SE2, SE3, Twist2, Twist3, UnitQuaternion
import matplotlib as mpl

mpl.interactive(True)

# %config ZMQInteractiveShell.ast_node_interactivity = 'last_expr_or_assign'

# skew symmetric matrix box 2D
skew(2)
# vex(_)

# skew symmetric matrix box 2D

skew([1, 2, 3])
# vex(_)

# %%
# simple comment
R = rot2(0.2)

det(R)

det(R*R)

# %%
# assfdsa dsfasf
# sdfasfd
#  dsfasdfasdf
#  sdfasf
# %% [markdown]
# markdown text goes here

# %%

theta = sym.symbol('theta')
R = rot2(theta)

simplify(R @ R)

sym.det(R).simplify()

## 2.1.1.2 2d matrix expon
R = rot2(0.3)

S = sp.linalg.logm(R)

vex(S)

sp.linalg.expm(S)

R = rot2(0.3)

R = sp.linalg.expm(  skew(0.3)  )

## blue box
S = skew(2)
vex(S)

# # 2.1.2.1 2D pose

plt.ion()

T1 = transl2(1, 2) @ trot2(30, 'deg')

plotvol2([0, 5, 0, 5])
trplot2(T1, frame='1', color='b')

T2 = transl2(2, 1)

trplot2(T2, frame='2', color='r')

T3 = T1 @ T2

trplot2(T3, frame='3', color='g')

T4 = T2 @ T1
trplot2(T4, frame='4', color='c')

P = np.r_[3, 2]

plot_point(P, label='P', textcolor='k', fillcolor='k')
P1 = np.linalg.inv(T1) @ np.r_[P, 1]

h2e( np.linalg.inv(T1) @ e2h(P) )

## 2.1.2.2 2D centres of rotation

plotvol2([-5, 4, -1, 4.5])
T0 = np.eye(3,3)
trplot2(T0, frame='0')
X = transl2(2, 3)
trplot2(X, frame='X')

R = trot2(2)

trplot2(R @ X, framelabel='RX', color='r')
trplot2(X @ R, framelabel='XR', color='r')

C = np.r_[1, 2]
plot_point(C, 'ko', label='C', textcolor='k', fillcolor='k')


RC = transl2(C) @ R @ transl2(-C)
trplot2(RC @ X, framelabel='XC', color='r')

## 2.1.2.3 2D twists
tw = Twist2.Revolute(C)

tw.exp(2)

tw.pole()

tw = Twist2.Prismatic([3, 4])

tw.exp(5)

T = transl2(2, 3) @ trot2(0.5)

tw = Twist2(T)
tw.SE2()

## 2.2.1.1 3D rotation
R = rotx(pi / 2)

plt.clf()
trplot(R)

tranimate(R)

# HACK tranimate(R, '3d')

R1 = rotx(pi/2) @ roty(pi/2)
trplot(R1)

R2 = roty(pi/2) @ rotx(pi/2)
trplot(R2)

## 3-angle representation
R = rotz(0.1) @ roty(0.2) @ rotz(0.3);

R = eul2r(0.1, 0.2, 0.3)

gamma = tr2eul(R)

R = eul2r(0.1 , -0.2, 0.3)

gamma = tr2eul(R)

# eul2r(_)
eul2r(gamma)

R = eul2r(0.1, 0, 0.3)

tr2eul(R)

# RPY angles
R = rpy2r(0.1, 0.2, 0.3, order="zyx")

gamma = tr2rpy(R)

R = rpy2r(0.1, 0.2, 0.3, order="xyz")

# tripleangle

## 2 vector
a = [1, 0, 0]
o = [0, 1, 0]
R = oa2r(o, a)

## angle vector
R = rpy2r(0.1 , 0.2, 0.3)

theta, v = tr2angvec(R)

e, x = np.linalg.eig(R)

theta = np.angle(e[0])

R = angvec2r(pi / 2, [1, 0, 0])

# # 3D matrix expon

R = rotx(0.3)

S = sp.linalg.logm(R) 

vex(S)

trlog(R, twist=True)

sp.linalg.expm(S)

R = rotx(0.3)

R = sp.linalg.expm( skew([1, 0, 0]) * 0.3 )

## blue box
S = skew([1, 2, 3])

vex(S)

## quaternions
q = UnitQuaternion( rpy2r(0.1, 0.2, 0.3)  )

q = q * q

q.inv()

q * q.inv()

q / q

q.R

q.plot()

q * [1, 0, 0]


## 2.2.2.1 hom xform
T = transl(2, 0, 0) @ trotx(pi/2) @ transl(0, 1, 0)

trplot(T)

t2r(T)

transl(T)

## 2.2.2.3 twists in 3d
tw = Twist3.Revolute([1, 0, 0], [0, 0, 0])

tw.exp(0.3)

tw = Twist3.Prismatic([0, 1, 0])

tw.exp(2)

X = transl(3, 4, -4)

tw = Twist3.Revolute([0, 0, 1], [2, 3, 2], 0.5)

angles = np.arange(0, 15, 0.3)
plt.clf()
trplot([tw.exp(theta).A @ X for theta in angles], style='rgb', width=2)

L = tw.line()


# ## 2.1.1.1 2d rotation
L.plot('k:', linewidth=2)

plt.show(block=True)

T = transl(1, 2, 3) @ eul2tr(0.3, 0.4, 0.5)
tw = Twist3(T)

tw.pitch()

tw.theta()

tw.pole()

## normalization
R = np.eye(3, 3)
np.linalg.det(R) - 1

for i in range(100):
       R = R @ rpy2r(0.2, 0.3, 0.4)
np.linalg.det(R) - 1

R = trnorm(R)
np.linalg.det(R) - 1

q = q.unit()

q2 = q  # ADDITION
q = q * q2

## more twists
tw = Twist3.Revolute([1, 0, 0], [0, 0, 0])

tw.S
tw.v
tw.w

tw.se3()

tw.exp(0.3)

tw.line()

t2 = tw * tw
tr2angvec(t2.SE3().A)

## using the toolboxes
T1 = SE2(1, 2, 30, unit='deg')
T1.shape

T1 

T1.A 
T1.A.shape

T1.inv() * P
