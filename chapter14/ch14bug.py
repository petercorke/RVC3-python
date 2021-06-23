#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## RVC2: Chapter 14 - sparse/BA bug

clear
close all
clc


im1=iread('walls-l.jpg',  'double', 'reduce', 2)
im2=iread('walls-r.jpg',  'double', 'reduce', 2)

sf1 = isurf(im1)
sf2 = isurf(im2)
## 
# 

m = sf1.match(sf2, 'top', 1000)

randinit
[H,r] = m.ransac(@homography, 4)

m.show

idisp(im1)
plot_point(m.inlier.p1, 'ws')

m = m.outlier
## 14.3.1 Sparse stereo



randinit
[F,r] = m.ransac(@fmatrix,1e-4, 'verbose')

cam = CentralCamera('image', im1)
cam.plot_epiline(F', m.inlier.subset[39].p2, 'y')

#
[~,md] = iread('walls-l.jpg')

f = md.DigitalCamera.FocalLength

md.Model


cam = CentralCamera('image', im1, 'focal', f/1000, ...
    'pixel', 2*1.5e-6)

E = cam.E(F)

T = cam.invE(E, [0,0,10]')

T.torpy('yxz', 'deg')

t = T.t
T.t = 0.3 * t/t[0]


r1 = cam.ray(m[0].p1)

r2 = cam.move(T).ray(m[0].p2)

[P,e] = r1.intersect(r2)
P'

e

m2 = m.inlier.subset[99]

r1 = cam.ray( m2.p1 )
r2 = cam.move(T).ray( m2.p2 )

[P,e] = r1.intersect(r2)

z = P(3,:)

idisp(im1)
plot_point(m2.p1, 'y*', 'textcolor', 'y', 'printf', {'#.1f', z})
## 14.4 Bundle adjustment

p1 = cam.project(P)
p2 = cam.move(T).project(P)

e = colnorm( [p1-m2.p1 p2-m2.p2] )

mean(e)
max(e)

#
ba = BundleAdjust(cam)

c1 = ba.add_camera( SE3[], 'fixed' )
c2 = ba.add_camera( T )

for j=1:length(m2)
    lm = ba.add_landmark( P(:,j) )
    ba.add_projection(c1, lm, m2(j).p1)
    ba.add_projection(c2, lm, m2(j).p2)
end

ba

ba.plot

x = ba.getstate
about x

x(7:12)

x(13:15)

ba.errors(x)

#[p,A,B] = cam.derivs(t, r, P)

baf = ba.optimize(x)

ba.getcamera[1].print('camera')
baf.getcamera[1].print('camera')

baf.getlandmark[4]'

ba.plot[]

e = sqrt( baf.getresidual[] )
about e

median( e(:) )

find( e(1,:) > 1 )

[mx,k] = max( e(1,:) )

