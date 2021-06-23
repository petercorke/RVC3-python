#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

#
# JB = -JA(1:3) 

cam = CentralCamera('default' )

t = [0 0 0]'
R = rpy2tr(0.3, 0.3, 0.4)
q = UnitQuaternion(R).double

T =  transl(t) * R

P = [1 2 5]'
[p0,vis] = cam.project(P, 'Tcam', T)

d = 0.001
dd = d*eye[2]

[UVS,JAS,JBS] = cameraModel(t[0], t[1], t[2], q[1], q[2], q[3], ...
    P[0], P[1], P[2], ...
    cam.f, cam.rho[0], cam.u0, cam.v0)

## projection
fprintf('-- test projection function\n')
fprintf(' toolbox\n')
p0
fprintf(' symbolic\n')
UVS

## jacobian B
fprintf('-- Jacobian B\n')
fprintf(' toolbox\n')
p1 = cam.project( bsxfun(@plus, P, dd), 'Tcam', T)

JB = bsxfun(@minus, p1, p0) / d

# symbolically derived result
fprintf(' symbolic\n')
JBS

## jacobian A

R = UnitQuaternion(q).R
T =  rt2tr(R, t)

JA = []
for i=1:3
    T =  rt2tr(R, t+dd(:,i))
    p = cam.project(P, 'Tcam', T)
    JA = [JA (p-p0)/d]
end

for i=1:3
    qq = q(2:4)
    qq(i) = qq(i) + d
    qs = sqrt(1-sum(qq.^2))
    RR = UnitQuaternion([qs qq]).R
    T =  rt2tr(RR, t)
    p = cam.project(P, 'Tcam', T)
    JA = [JA (p-p0)/d]
end

fprintf('-- Jacobian A\n')
fprintf(' toolbox\n')
JA

# symbolically derived result
fprintf(' symbolic\n')
JAS

## test the quaternion vector update
fprintf('-- Quaternion vector update\n')

#numerically
q1 = UnitQuaternion.rpy(.2, .3, .4)
q2 = UnitQuaternion.rpy(.3, -0.2, 0.2)
qq = q1*q2
qq.v

# symbolic solution
args = num2cell([q1.v q2.v])
qvmul(args{:})

# # lets do it numerically with quaternion reconstruction
# v1 = q1.v
# v2 = q2.v
# s1 = sqrt(1-sum(v1.^2))
# s2 = sqrt(1-sum(v2.^2))
# qq1 = Quaternion([s1 v1])
# qq2 = Quaternion([s2 v2])
# qqq = qq1*qq2
# qqq.v




