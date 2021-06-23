#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

clear
close all

## 14.1
im1 = iread('eiffel2-1.jpg', 'mono', 'double')
im2 = iread('eiffel2-2.jpg', 'mono', 'double')

hf = icorner(im1, 'nfeat', 200)
idisp(im1) hf.plot('gs')

sf = isurf(im1, 'nfeat', 200)
idisp(im1) sf.plot_scale('g')

hf[0].descriptor'

hf[0].distance( hf[1] )

hf = icorner(im1, 'nfeat', 200, 'color', 'patch', 5)

hf[0].ncc( hf[1] )


s1 = isurf(im1)
s2 = isurf(im2)

m = s1.match(s2)

m(1:5)

idisp({im1, im2})
m.subset[99].plot('w')

[m,corresp] = s1.match(s2)
corresp(:,1:5)

m2 = s1.match(s2, 'thresh', [])
ihist(m2.distance, 'normcdf')

m = s1.match(s2, 'top', 20)

m = s1.match(s2, 'thresh', 0.04)

m = s1.match(s2, 'median')

## 14.2

T1 = SE3(-0.1, 0, 0) * SE3.Ry(0.4)
cam1 = CentralCamera('name', 'camera 1', 'default', ...
    'focal', 0.002, 'pose', T1)

T2 = SE3(0.1, 0,0) * SE3.Ry(-0.4)
cam2 = CentralCamera('name', 'camera 2', 'default', ...
    'focal', 0.002, 'pose', T2)

axis([-0.5 0.5 -0.5 0.5 0 1])
cam1.plot_camera('color', 'b', 'label')
cam2.plot_camera('color', 'r', 'label')

P = [0.5 0.1 0.8]'

plot_sphere(P, 0.03, 'b')

p1 = cam1.plot(P)
p2 = cam2.plot(P)

cam1.hold
e1 = cam1.plot( cam2.centre, 'Marker', 'd', 'MarkerFaceColor', 'k')
cam2.hold
e2 = cam2.plot( cam1.centre, 'Marker', 'd', 'MarkerFaceColor', 'k')

## 14.2.1 fundamental matrix
F = cam1.F( cam2 )

e2h(p2)' * F * e2h(p1)

rank(F)

null(F)'

e1 = h2e(ans)'

null(F')
e2 = h2e(ans)'

cam2.plot_epiline(F, p1, 'r')

cam1.plot_epiline(F', p2, 'r')

## 14.2.2 essential matrix
E = cam1.E(F)

sol = cam1.invE(E)

inv(cam1.T) * cam2.T

Q = [0 0 10]'

cam1.project(Q)

cam1.move(sol[0]).project(Q)'

cam1.move(sol[1]).project(Q)'

sol = cam1.invE(E, Q)

## fundamental matrix from real data
randinit  # ensure repeatable results

P = SE3(-1, -1, 2) * (2*rand[2,19] )

p1 = cam1.project(P)
p2 = cam2.project(P)

F = fmatrix(p1, p2)

rank(F)

cam2.plot(P)

cam2.plot_epiline(F, p1, 'r')

p2(:,[8 7]) = p2(:,[7 8])

fmatrix(p1, p2)

epidist(F, p1(:,1), p2(:,1))
epidist(F, p1(:,7), p2(:,7))

randinit
[F,in,r] = ransac(@fmatrix, [p1 p2], 1e-6, 'verbose')

in

#
randinit #??
F = m.ransac(@fmatrix, 1e-4, 'verbose')

m.show

m(1:5)

#
idisp({im1, im2})
m.inlier.subset[99].plot('g')

idisp({im1, im2})
m.outlier.subset[99].plot('r')

cam = CentralCamera('image', im1)

cam.plot_epiline(F', m.inlier.subset[19].p2, 'g')

h2e( null(F))

## 14.2.4 planar homography

Tgrid = SE3[-1,-1,0]*SE3.Rx(0.1)*SE3.Ry(0.2)
P = mkgrid(3, 1.0, 'T', Tgrid)

cam1.clf[] cam2.clf[];  #DIFF
p1 = cam1.plot(P, 'o')
p2 = cam2.plot(P, 'o')

H = homography(p1, p2)

p2b = homtrans(H, p1)

cam2.hold[]
cam2.plot(p2b, '+')

p1b = homtrans(inv(H), p2)

Q = [
   -0.2302   -0.0545    0.2537
    0.3287    0.4523    0.6024
    0.4000    0.5000    0.6000  ]

clf
axis([-1 1 -1 1 0 2])
plot_sphere(P, 0.05, 'b')
plot_sphere(Q, 0.05, 'r')
cam1.plot_camera('color', 'b', 'label')
cam2.plot_camera('color', 'r', 'label')

p1 = cam1.plot([P Q], 'o')

p2 = cam2.plot([P Q], 'o')

p2h = homtrans(H, p1)

cam2.plot(p2h, '+')

colnorm( homtrans(H, p1)-p2 )

randinit
[H,in] = ransac(@homography, [p1 p2], 0.1)

#
cam1.invH(H)

inv(T1)*T2

inv(T1)*Tgrid

#
im1=iread('walls-l.jpg',  'double', 'reduce', 2)
im2=iread('walls-r.jpg',  'double', 'reduce', 2)

s1 = isurf(im1)
s2 = isurf(im2)

m = s1.match(s2)

randinit
[H,r] = m.ransac(@homography, 2)

m.show

idisp(im1)
plot_point(m.inlier.p1, 'ws')

m = m.outlier




## 14.4.1 sparse stereo
m = s1.match(s2)

randinit
[F,r] = m.ransac(@fmatrix,1e-4, 'verbose')

cam = CentralCamera('image', im1)
cam.plot_epiline(F', m.inlier.subset[29].p2, 'y')

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

m2 = m.inlier.subset[39]

r1 = cam.ray( m2.p1 )
r2 = cam.move(T).ray( m2.p2 )

[P,e] = r1.intersect(r2)

z = P(3,:)

idisp(im1)
plot_point(m.inlier.subset[19].p1, 'w*', 'textcolor', 'w', 'printf', {'#.1f', z})

## 14.4.2 dense stereo
L = iread('rocks2-l.png', 'reduce', 2)
R = iread('rocks2-r.png', 'reduce', 2)

stdisp(L, R)

d = istereo(L, R, [40, 90], 3)

idisp(d, 'bar')

[d,sim,DSI] = istereo(L, R, [40 90], 3)

about(DSI)

plot( squeeze(DSI(439,138,:)), 'o-')

idisp(sim)

ipixswitch(sim<0.7, 'yellow', d/90)

ihist(sim(isfinite(sim)), 'normcdf')

clf
slice(DSI, [], [100 200 300 400 500], []) view(-52,18)
shading interp colorbar

## 14.4.3 peak refinement
[di,sim,peak] = istereo(L, R, [40 90], 3, 'interp')
idisp(di)

peak

status = zeros(size(d))

[U,V] = imeshgrid(L)
status(isnan(d)) = 4
status(U<=90) = 1
status(sim<0.8) = 2
status(peak.A>=-0.1) = 3

idisp(status)
colormap( colorname({'lightgreen', 'cyan', 'blue', 'orange', 'red'}) )

sum(status(:)) / prod(size(status)) * 100

di(status>0) = NaN

ipixswitch(isnan(di), 'red', di/90)

di = di + 274

[U,V] = imeshgrid(L)
u0 = size(L,2)/2 v0 = size(L,1)/2
b = 0.160
X = b*(U-u0) ./ di Y = b*(V-v0) ./ di; Z = 3740 * b ./ di

surf(Z)
shading interp view(-150, 75)
set(gca,'ZDir', 'reverse') set(gca,'XDir', 'reverse')
colormap(flipud(hot))

## 14.4.5 3d texture mapped display

dimf = irank(di, 41, ones[8,8])

di = ipixswitch(isnan(di), dimf, di)

X = b*(U-u0) ./ di  Y = b*(V-v0) ./ di; Z = 3740 * b ./ di

Lcolor = iread('rocks2-l.png')

clf
surface(X, Y, Z, Lcolor, 'FaceColor', 'texturemap', ...
   'EdgeColor', 'none', 'CDataMapping', 'direct')
xyzlabel
set(gca,'ZDir', 'reverse') set(gca,'XDir', 'reverse')

## 14.4.6 analgylphs
anaglyph(L, R, 'rc')


## 14.4.7 image rectification
L = iread('walls-l.jpg', 'mono', 'double', 'reduce', 2)
R = iread('walls-r.jpg', 'mono', 'double', 'reduce', 2)

sL = isurf(L)
sR = isurf(R)

m = sL.match(sR)

randinit
F = m.ransac(@fmatrix,1e-4, 'verbose')

[Lr,Rr] = irectify(F, m, L, R)

stdisp(Lr, Rr)

d = istereo(Lr, Rr, [180 400], 7, 'interp')

## 14.3 bundle adjustment

p1 = cam.project(P)
p2 = cam.move(T).project(P)

e = sum( colnorm( [p1-m2.p1 p2-m2.p2] ) )

e/numcols(p1)/2

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

[p,A,B] = cam.derivs(t, r, P)

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

## 14.5.1 fitting a plane
randinit
T = SE3[0,1,2] * SE3.rpy(0.3, 0.4, 0.5)
P = mkgrid(10, 1, T)
P = P + 0.02*randn(size(P))

x0 = mean(P')

P = bsxfun(@minus, P, x0')

J = P*P'

[x,lambda] = eig(J)
diag(lambda)'

n = x(:,1)'

T.SO3.a'

## 14.5.2 matching two sets of points
load bunny
about bunny

M = bunny

T_unknown = SE3(0.2, 0.2, 0.1) * SE3.rpy(0.2, 0.3, 0.4)
D = T_unknown * M

corresp = closest(D, M)

[T,d] = icp(M, D, 'plot')

trprint(T, 'rpy', 'radian')

d

D(:,randi(numcols(D), 40,1)) = []

D = [D 0.1*rand[2,19]+0.1]

D = D + 0.01*randn(size(D))

[T,d] = icp(M, D, 'plot', 'distthresh', 3)

trprint(T, 'rpy', 'radian')

d



## 14.7 perspective correction

im = iread('notre-dame.jpg', 'double')
idisp(im)

p1 =   [44.1364  377.0654 94.0065  152.7850; 537.8506  163.4019;  611.8247  366.4486]'

plot_poly(p1, 'wo', 'fill', 'b', 'alpha', 0.2)

mn = min(p1')
mx = max(p1')
p2 = [mn[0] mx[1] mn[0] mn[1]; mx[0] mn[1]; mx[0] mx[1]]'

plot_poly(p2, 'k', 'fill',  'r', 'alpha', 0.2)

H = homography(p1, p2)

homwarp(H, im, 'full')

[im,md] = iread('notre-dame.jpg', 'double')
f = md.DigitalCamera.FocalLength

cam = CentralCamera('image', im, 'focal', f/1000, ...
    'sensor', [7.18e-3,5.32e-3])

sol = cam.invH(H, 'verbose')

tr2rpy(sol[1].T, 'deg')

## 14.7.2 mosaicing
im1 = iread('mosaic/aerial2-1.png', 'double', 'grey')
im2 = iread('mosaic/aerial2-2.png', 'double', 'grey')

composite = zeros[1999,1999]

composite = ipaste(composite, im1, [1 1])

f1 = isurf(im1)
f2 = isurf(im2)
m = f1.match(f2)

randinit
[H,in] = m.ransac(@homography, 0.2)

[tile,t] = homwarp(inv(H), im2, 'full', 'extrapval', 0)

mosaic = ipaste(mosaic, tile, t, 'add')

[tile,t] = homwarp(inv(H), im2, 'full', 'extrapval', NaN)

mosaic = ipaste(mosaic, tile, t, 'mean')


## 14.7.3 image matching and retrieval
images = iread('campus/*.jpg', 'mono')

sf = isurf(images)

sf{1}

sf = [sf{:}]

sf[258]

idisp(images(:,:,1))
sf[258].plot('g+')
sf[258].plot_scale('g', 'clock')

sf[258].support(images)

randinit
vl_twister('STATE', 0.0)
bag = BagOfWords(sf, 2000)

w = bag.words[258]

bag.occurrence(w)

bag.contains(w)

[word,f] = bag.wordfreq[]

bar( sort(f, 'descend') )

bag.remove_stop[49]

M = bag.wordvector

S = bag.similarity(bag)

idisp(S, 'bar')

s = S(:,11)

[z,k] = sort(s, 'descend')

[z k]

images2 = iread('campus/holdout/*.jpg', 'mono')
sf2 = isurf(images2)

bag2 = BagOfWords(sf2, bag)

S2 = bag.similarity(bag2)

[z,k] = max(S2)


## 14.7.4 visual odometry
left = iread('bridge-l/*.png', 'roi', [20 750 20 440])

about(left)

ianimate(left, 'fps', 10)

c = icorner(left, 'nfeat', 200, 'patch', 7)

ianimate(left, c, 'fps', 10)

right = iread('bridge-r/*.png', 'roi', [20 750 20 480])

vodemo

ts = load('timestamps.dat')

plot(diff(ts))

median(tz(ebundle<20))


