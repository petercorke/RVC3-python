## RVC2: Chapter 12 - Images and Image Processing
import numpy as np
import scipy as sp
from math import pi
from spatialmath import SE3
from spatialmath.base import e2h, h2e, plot_sphere
from machinevisiontoolbox import *


# TODO
# lookup numpy uint88 type and divsion rules
# .chromaticity()
#chroma = subject.chromaticity()

# this is another image with r, g planes
# all bool ops give 0/1 images
# video reader is a generator
# .clip(min, max)
# K = Kernel.Box(20)  
# K = Kernel.Gauss(4)
# .apply(func)
#th.width_range(20), th.height_range(20),
# .roi(start, end) tuples
# .roi(sx, ex, sy, ey)
# .roi(box object)
# .similarity(T, method) how done in OpenCV?
# randinit

# Image() constructor from ndarray accepts a shape argument
# rank filter, rank filter over a mask
# tag images as binary
# pickregion returns roi as array
# planes are a dict, can be multi letter
# extent of image is kept or defaults

## 12.1.1  Images from files

street, _ = iread('street.png')
type(street)
street.shape

street

street[199,299]

idisp(street)

a = np.uint8(99)                                                              

b = np.uint8(199)

a +  b
a - b

a / b
a // b

street = Image.Read('street.png')
print(street.shape, street.image.shape)
street.disp()

#TODO:
# iread/idisp use BGR order by default
# iread strip the A plane
# colorize alpha=x

flowers, _ = iread('flowers8.png')
type(flowers)
flowers.shape
idisp(flowers[:, :, 2])

flowers = Image.Read('flowers8.png')
flowers

pix = flowers.image[276, 318, :]

flowers = Image.Read('flowers8.png')
print(flowers.shape, flowers.image.shape)
flowers.disp()
flowers.red().disp()

seq = Image.Read('seq/*.png')
seq
seq[3]
seq[3].disp()

# TODO: perhaps use that package directly
# md = Image.ReadMetaData('church.jpg')
# md

## 12.1.2  Images from an attached camera

# camera = LocalCamera()
# VideoCamera('?')

# cam = VideoCamera('macvideo')

# cam.size[]

# im = cam.grab[]

#enable this code if you have a camera and Image Acquisition Toolbox + appropriate Hardware Support Package

## 12.1.3  Images from a movie file

# video = Video('traffic_sequence.mpg')
# video

# im = video.grab()

# while frame in video:
#     frame.disp()

# ## 12.1.4  Images from the web

# cam = AxisWebCamera('http://wc2.dartmouth.edu')

# cam.size[]

# im = cam.grab[]

# ## 12.1.5  Images from maps

# ev = EarthView[] #DIFF

# ev.grab(-27.475722,153.0285, 17)

# ev.grab('QUT brisbane', 17)

# ev.grab(-27.475722,153.0285, 15, 'map')

# ev.grab(-27.475722,153.0285, 15, 'roads')

## 12.1.6  Images from code

im = Image.Pattern('rampx', 256, 2)
im = Image.Pattern('siny', 256, 2)
im = Image.Pattern('squares', 256, 50, 25)
im = Image.Pattern('dots', 256, 256, 100)

canvas = Image.Zeros(1000, 1000)

sq1 = 0.5 * Image.Ones(150, 150)
sq2 = 0.9 * Image.Ones(80, 80)

canvas = canvas.paste(sq1, (100, 100))
canvas = canvas.paste(sq2, (300, 300))

circle = 0.6 * Image(Kernel.Circle(120))

circle.shape

canvas = canvas.paste(circle, (600, 200))

canvas = canvas.line((100, 100), (800, 800), 0.8)

canvas.disp()

## 12.2  Image histograms

church = Image.Read('church.png', grey=True)
h = church.hist()
h.plot(block=True)

# TODO
# x = h.peak()

# x = hist.peak(scale=25)

## 12.3  Monadic operations

imd = church.asfloat()

im = imd.asint()

grey = flowers.grey()

color = grey.colorize()

color = grey.colorize([1, 0, 0])

bright = church >= 180
bright
bright.disp()

church.stretch().disp()

# TODO church.normhist().disp()

# church.hist('cdf').plot()

church.gamma_decode(1 / 0.45)
church.gamma_decode('sRGB')


(church // 64 ).disp()

## 12.4  Diadic operations

subject = Image.Read('greenscreen.png', dtype='float', gamma='sRGB')

chroma = subject.chromaticity()

# this is another image with r, g planes

# TODO
chroma.plane('g').hist().plot()

mask = chroma.plane('g') < 0.45
mask.disp()

# this image has bool values

mask3 = mask.colorize()

(mask3 * subject).disp()

bg = Image.Read('road.png', dtype='float')

# TODO interp2d
# bg = bg.samesize(subject)

# (bg * (1 - mask3)).disp()

# (subject * mask3  + bg * (1 - mask3))

# Image.which(mask, subject, bg)

#

# traffic = Movie('traffic_sequence.mpg', grey=True, dtype='float')
# bg = traffic.grab()
# sigma = 0.02
# for frame in traffic:
#     diff = frame - bg
#     bg += diff.clip(-sigma, sigma)
#     bg.disp()


## 12.5.1.1  Smoothing

K = np.ones((20, 20)) / 21 ** 2
mona = Image.Read('monalisa.png', grey=True, dtype='float')
mona.convolve(K).disp()

K = Kernel.Box(20)

K = Kernel.Gauss(4)
mona.convolve(K).disp()

mona.smooth(5).disp()
# TODO what does 5 mean

# plt.plot_surface(-15:15, -15:15, K)

K = Kernel.Circle(8, hw=15)

## 12.5.1.3  Edge detection

castle = Image.Read('castle.png', grey=True, dtype='float')

profile = castle.image[360,:]

plt.plot(profile)

K = [0.5, 0, -0.5]
castle.convolve(K).disp(colormap='invsigned')

Du = Kernel.Sobel()

castle.convolve(Du).disp(colormap='invsigned')
castle.convolve(Du.T).disp(colormap='invsigned')

sigma = 1
Gu = Du.smooth(std=sigma)

deriv = Kernel.DGauss(1)
Iu = castle.convolve(deriv)
Iv = castle.convolve(deriv.T)

# m = (Iu ** 2 + Iv ** 2).sqrt()
# m = Image.map(lambda x, y: sqrt(x ** 2 + y ** 2), Iu, Iv)
m = Image.Apply(np.sqrt, Iu ** 2 + Iv ** 2)
m = (Iu ** 2 + Iv ** 2).apply(np.sqrt)


# th = np.arctan2( Iv, Iu)
th = Image.Apply(np.arctan2, Iv, Iu)
th = Iv.apply(np.arctan2, Iu)

# plt.quiver(1:20:numcols(th), 1:20:numrows(th), ...
#        Iu(1:20:end,1:20:end), Iv(1:20:end,1:20:end))
# plt.quiver(np.arange(0, th.width, 20), np.arange(0, th.height, 20),
#     Iu[0:20:, 0:20:], Iv[0:20:, 0:20:])

plt.quiver(th.width_range(20), th.height_range(20),
    Iu[0:20:, 0:20:], Iv[0:20:, 0:20:])

gradient = castle.sobel(Kernel.DGauss(1))

edges = castle.Canny(2)

L = Kernel.Laplace()

laplace = castle.convolve(Kernel.LoG(1))

profile = laplace.image[360, 570: 600]
plt.plot(np.arange(360, 570), profile, '-o')

zc = laplace.zerocross()

## 12.5.2  Template matching

mona = Image.Read('monalisa.png', grey=True, dtype='float')
T = mona.roi((170, 220), (245, 295))

sad(T, T)
ssd(T, T)
ncc(T, T)

sad(T, T * 0.9)
ssd(T, T * 0.9)
ncc(T, T * 0.9)

sad(T, T + 0.1)
ssd(T, T + 0.1)
ncc(T, T + 0.1)

zsad(T, T + 0.1)
zssd(T, T + 0.1)
zncc(T, T + 0.1)

zncc(T, T * 0.9 + 0.1)

# wally
crowd = Image.Read('wheres-wally.png', dtype='float')
crowd.disp()

wally = Image.Read('wally.png', dtype='float')
wally.disp()

S = crowd.similarity(wally, zncc)

S.disp(colormap='jet', colorbar=True)

p, mx = S.peak2(1, npeaks=5)
mx

idisp(crowd)
plot_circle(p, 30, 'edgecolor', 'g')
plot_point(p, label=' {:}', fontsize=24, color='y', markersize='none')


## 12.5.3  Nonlinear operations

out = mona.windowmap((6, 6), np.linalg.std)

mx = mona.rank(rank=0, width2=2)

med = mona.rank(rank=11, width2=2)

np.random.seed(0)
mona = Image.Read('monalisa.png', grey=True, dtype='float').column()
npix = mona.npixels
spotty[np.random.randint(0, npix)] = 0
spotty[np.random.randint(0, npix)] = 1
spotty = Image(spotty, shape=mona.shape)
spotty.disp()

spotty.rank(rank=4, width2=1).disp()

#

M = np.ones(3)
M[1,1] = 0
mxn = lena.rank(M, rank=1)

(lena > mxn).disp()


## 12.6  Mathematical morphology

im = Image.Read('morph-demo1.png')
im.disp()

S = np.ones(5, 5)

mn = im.morph('minimum', S)

# %run morphdemo im S 'min'

mx = im.morph('maximum', S)

out = im.erode(S)
out = im.dilate(S)

## 12.6.1  Noise removal

objects = Image.Read('segmentation.png')

S = Kernel.Circle(3)

clean = objects.close(S).open(S)

closed = objects.open(S).close(S)

## 12.6.2  Boundary detection

eroded = clean.morph(Kernel.Circle(1), 'minimum')

(clean-eroded).disp()

## 12.6.3  Hit or miss transform

out = image.hitormiss(S)

skeleton = clean.thin()

ends = skeleton.endpoint()

joins = skeleton.triplepoint()

## 12.6.4  Distance transform

im = Pattern.Squares(256, 256, 128).rotate(-0.3)
edges = im.canny() > 0

dx = edges.distancexform('euclidean')
idisp(dx)


## 12.7.1  Cropping

mona = Image.Read('monalisa.png')

roi = mona.pickregion()

eyes = mona.roi(roi)
idisp(eyes)

smile = mona.roi([265, 342, 264, 286])
smile.disp()

## 12.7.2  Image resizing

roof = Image.Read('roof.jpg', 'grey')

smaller = roof.image[:7:, :7:]

smaller =  room.subsample(7)

bigger = smaller.replicate(7)

smoother = bigger.smooth(4)

smaller = mona.scale(0.1)
bigger = smaller.scale(10)

## 12.7.3  Image pyramids

p = mona.grey.pyramid(10)

## 12.7.4  Image warping

mona = Image.Read('monalisa.png', 'double', 'grey')

Up, Vp = Image.meshgrid((400, 400))

U = 4 * (Up - 100)
V = 4 * (Vp - 200)

little_mona = mona.interp2(U, V)
little_mona.disp()


points = meshgrid((400, 400), points=True)
T = Twist2.Revolute((256, 256), pi / 6)
points = T * points

twisted_mona = mona.interp2(points)
twisted_mona.disp()

twisted_mona = mona.rotate(pi / 6)
twisted_mona.disp()

##
distorted = Image.Read('Image18.tif', dtype='float')

Up, Vp = distorted.meshgrid()

# load bouget
k = kc[[1, 2, 5]]
p = kc[[3, 4]]
u0 = cc[0]
v0 = cc[1]
fpix_u = fc[0]
fpix_v = fc[1]

u = (Up - u0) / fpix_u
v = (Vp - v0) / fpix_v

r = np.sqrt(u ** 2 + v ** 2)

Δu = u * (k[0] * r ** 2 + k[1] * r ** 4 + k[2] * r **6) + \
   2 * p[0] * u * v + p[1] * (r ** 2 + 2 * u ** 2)
Δv = v * (k[0] * r ** 2 + k[1] * r ** 4 + k[2] * r ** 6) + \
   p[0] * (r ** 2 + 2 * v ** 2) + 2 * p[0] * u * v

ud = u + Δu
vd = v + Δv

U = ud * fpix_u + u0
V = vd * fpix_v + v0

undistorted = distorted(U, V)
undistorted.disp()
