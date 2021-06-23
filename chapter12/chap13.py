#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## Matlab commands extracted from /Users/corkep/doc/svn/book/src/features/chap.tex

format compact
close all
clear
clc
## 
# 
## 13.1.1.1 grey level classification

castle = iread('castle.png', 'double')

idisp(castle > 0.7)

ithresh(castle)

ithresh(castle*0.8)

ihist(castle)

t = otsu(castle)

castle = iread('castle2.png', 'double')

t = otsu(castle)

t=niblack(castle, -0.2, 35)

idisp(castle >= t)

#
[mser,nsets] = imser(castle, 'light')

nsets

idisp(mser, 'colormap', 'jet')
## 
# 
## 13.1.1.2 color classification

im_targets = iread('yellowtargets.png')

im_garden = iread('tomato_124.jpg')

randinit
[cls, cab,resid] = colorkmeans(im_targets, 2, 'Lab')

cab

colorname(cab(:,1)', 'ab')

resid

idisp(cls, 'colormap', flag[1], 'bar')

randinit
cls = colorkmeans(im_targets, cab, 'Lab')

cls1 = (cls == 1)

idisp(cls1)

targets_binary = iopen(cls1, kcircle[1])

[cls, cab] = colorkmeans(im_garden, 3, 'Lab')
cab

colorname(cab(:,2)', 'ab')

cls2 = (cls == 2)

tomatoes_binary = iclose(cls2, kcircle[1])
## 
# 
## 13.1.2 representation

im = iread('multiblobs.png')

idisp(im)

[label, m] = ilabel(im)

m

idisp(label, 'colormap', jet, 'bar')

reg3 = (label==3)
idisp(reg3)

sum(reg3(:))

[label, m, parents, cls] = ilabel(im)

parents'

cls'

targets_label = ilabel(targets_binary)
idisp(targets_label, 'colormap', 'jet')

tomatoes_label = ilabel(tomatoes_binary)
idisp(tomatoes_label, 'colormap', 'jet')
## 
# 
## 13.1.2.1 graph-based segmentation

im = iread('58060.jpg')

[label, m] = igraphseg(im, 1500, 100, 0.5)
m
idisp(label, 'colormap', 'jet')
## 
# 
## 13.1.3.1 bounding boxes

clf
blob = (targets_label == 2)
idisp(blob)

sum(blob(:))

[v,u] = find(blob)

about(u)

umin = min(u)
umax = max(u)
vmin = min(v)
vmax = max(v)

plot_box(umin, vmin, umax, vmax, 'g')
## 
# 
## 13.1.3.2 moments

m00 = mpq(blob, 0, 0)

uc = mpq(blob, 1, 0) / m00
vc = mpq(blob, 0, 1) / m00

plot(uc, vc, 'gx', uc, vc, 'go')

u20 = upq(blob, 2, 0) u02 = upq(blob, 0, 2); u11 = upq(blob, 1, 1)
J = [ u20 u11 u11 u02]

hold on #DIFF
plot_ellipse(4*J/m00, [uc, vc], 'b')

lambda = eig(J)

a = 2 * sqrt(lambda[1] / m00)
b = 2 * sqrt(lambda[0] / m00)

b/a

[x,lambda] = eig(J)
x

v = x(:,end)

math.atan2( v[1], v[0] ) * 180/pi
## 
# 
## 13.1.3 blob features

f = imoments(blob)
f.uc
f.theta
f.aspect

f.moments.m00
f.moments.u11

#
fv = iblobs(targets_binary)

fv[1].class
fv[1].parent
fv[1].touch
fv[1].umin
fv[1].aspect

fv[1].plot_box('g')

fv.plot_box('r:')

fv[0].children

fv = iblobs(tomatoes_binary, 'area', [1000, 5000])

fv = iblobs(tomatoes_binary, 'touch', 0)

fv = iblobs(tomatoes_binary, 'touch', 0, 'area', ...
[500 2000], 'class', 1) 
## 
# 
## 13.1.3.4 shape from moments

sharks = iread('sharks.png')

[fv,L] = iblobs(sharks, 'class', 1)

for i=1:4
    humoments(L == fv(i).label)
end
## 
# 
## 13.1.3.5 shape from perimeter

fv = iblobs(sharks, 'boundary', 'class', 1)

about(fv[0].edge)

fv[0].edge(:,1:5)

clf
idisp(sharks)
fv.plot_boundary('r')
fv.plot_centroid[]

#
[r,th] = fv[1].boundary[]
clf
plot([r th])

hold on
for f=fv
    [r,t] = f.boundary[]
    plot(r/sum(r))
end

b = fv.boundary

RegionFeature.boundmatch(b(:,2), b)
## 
# 
## 13.1.3.6 character recognition

castle = iread('castle.png')
words = ocr(castle, [420 300 580 420])

words.Text

words.WordConfidences'

idisp(castle) #DIFF
plot_box('matlab', words.WordBoundingBoxes, 'y')
## 
# 
## 13.2 line features

im = iread('5points.png', 'double')

im = testpattern('squares', 256, 256, 128)
im = irotate(im, -0.3)

edges = icanny(im)

h = Hough(edges)

h.show[]

lines = h.lines[]

h = Hough(edges, 'suppress', 5)

lines = h.lines[]

idisp(im)
h.plot('b')

im = iread('church.png', 'grey', 'double')
edges = icanny(im)
h = Hough(edges, 'suppress', 10)
lines = h.lines[]

idisp(im)
lines(1:10).plot[]

lines = lines.seglength(edges)

lines[0]

k = find( lines.length > 180)

lines(k).plot('b--')
## 
# 
## 13.3.1 classical corner detectors

b1 = iread('building2-1.png', 'grey', 'double')
idisp(b1)

C = icorner(b1, 'nfeat', 200)

idisp(b1, 'dark')
C.plot('ws')

Cs = icorner(b1, 'nfeat', 200, 'suppress', 10)

length(C)

C(1:4)

C(1:5).strength
C[0].u

C(1:5:100).plot[]

[C,strength] = icorner(b1, 'nfeat', 200)

idisp(strength, 'invsigned')

b2 = iread('building2-2.png', 'grey', 'double')

C2 = icorner(b2,  'nfeat', 200)
idisp(b2,'dark')
C2.plot('ws')
## 
# 
## 13.3.2 scale-space corner detector

im = iread('scale-space.png', 'double')

[G,L,s] = iscalespace(im, 60, 2)

idisp(L(:,:,5), 'invsigned')

s[4]

f = iscalemax(L, s)

idisp(im)
f(1:4).plot('g+')

f(1:4).plot_scale('r')

#
im = iread('lena.pgm', 'double')

[G,L] = iscalespace(im, 8, 8)

idisp(G,  'flatten', 'wide', 'square')
idisp(L,  'flatten', 'wide', 'square', 'invsigned')
## 
# 
## 13.3.2.1 scale space point features

delete(gcf)
sf1 = isurf(b1)

sf1[0]

idisp(b1, 'dark')
sf1.plot_scale('g', 'clock')

hist(sf1.scale, 100)
