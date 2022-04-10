# ------ standard imports ------ #

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import cv2 as cv

import ansitable
ansitable.options(unicode=True)

from spatialmath import *
from spatialmath.base import *
BasePoseMatrix._color=False
from roboticstoolbox import *

from spatialmath.base import *
import math
from math import pi

from machinevisiontoolbox import *
from machinevisiontoolbox.base import *

np.set_printoptions(
    linewidth=120, formatter={
        'float': lambda x: f"{0:8.4g}" if abs(x) < 1e-10 else f"{x:8.4g}"})

np.random.seed(0)
cv.setRNGSeed(0)

# ------------------------------ #


# Obtaining an Image


# Images from Files

street, _ = iread("street.png");
street
street.shape
street[400, 200]
idisp(street);
flowers, _ = iread("flowers8.png")
flowers.dtype
idisp(flowers);
flowers.shape
idisp(flowers[:, :, 0]);
pix = flowers[276, 318, :]
street = Image.Read("street.png")
street.shape
street.disp();
street.min()
street.max()
street.stats()
img = street.image;
type(img)
street.image[400, 200]
subimage = street.image[100:200, 200:300];
type(subimage)
subimage = street[100:200, 200:300];
type(subimage)
flowers = Image.Read("flowers8.png")
flowers.stats()
flowers.image[276, 318, :]
flowers.image[:, :, 0];
flowers[:, :, 0].disp();
flowers.plane(0).disp();
flowers.plane("R").disp();
flowers.red().disp();
flowers.plane("B:R:G")
flowers.plane("B:G:R").disp();

# Images from File Sequences

images = ImageCollection("seq/*.png");
len(images)
images[3]
images = ZipArchive("bridge-l.zip", "*.pgm");
len(images)

# Images from an Attached Camera

camera = VideoCamera(0)
camera.release()
image = camera.grab()

# Images from a Video File

video = VideoFile("traffic_sequence.mp4")
video.shape

# Images from the Web

dartmouth = WebCam("https://webcam.dartmouth.edu/webcam/image.jpg");
dartmouth.grab().disp();

# Images from Space

world = EarthView();
world.grab(-27.475722, 153.0285, 17).disp();
world.grab(-27.475722,153.0285, 15, type="map").disp();
world.grab(-27.475722,153.0285, 15, type="roads").disp();

# Images from Code

image = Image.Ramp(cycles=2, size=500, dir="x");
image = Image.Sin(cycles=5, size=500, dir="y");
image = Image.Squares(number=5, size=500);
image = Image.Circles(number=2, size=500);
canvas = Image.Zeros(1000, 1000, dtype="uint8")
canvas.draw_box(lt=(100, 100), wh=(150, 150), color=100, thickness=-1);
canvas.draw_box(lt=(300, 300), wh=(80, 80), color=150, thickness=-1);
canvas.draw_circle((600, 600), 120, color=200, thickness=-1)
canvas.draw_line((100, 100), (800, 800), color=250, thickness=8)
canvas.disp();

# Pixel Value Distribution

church = Image.Read("church.png", mono=True)
church.min()
church.max()
church.mean()
church.median()
church.std()
church.stats()
h = church.hist()
h.plot();
h.plot("ncdf", color="blue")
x = h.peaks();
x.shape
x = h.peaks(scale=25)

# Monadic Operations

church_float = church.to("float")
church.max()
church_float.max()
church_float.to("uint8")
street_float = Image.Read("street.png", dtype="float")
gray = flowers.mono()
color = gray.colorize()
color = gray.colorize((1, 0, 0))
bright = (church >= 180)
bright.disp();
church.stretch().stats()
im = church.normhist();
im = church.gamma_decode(1 / 2.2);
im = church.gamma_decode("sRGB");
(church // 64).disp();
church.npixels
church.apply(lambda x: x // 64).disp();
lut = [x // 64 for x in range(256)];  # create posterization lookup table
church.LUT(lut).disp();

# Diadic Operations

church / 2       # new Image with all pixel values halved
church + 20      # new Image with all pixel values increased by 20
church - church  # new Image with all pixel values equal to 0
church.apply2(church, lambda x, y: x - y).disp();
a = np.uint8(100)
b = np.uint8(200)
a + b
a - b
-a
a / b

# Applications


# Application: Chroma Keying

foreground = Image.Read("greenscreen.png", dtype="float")
cc = foreground.gamma_decode("sRGB").tristim2cc()
cc.plane("g").hist().plot()
mask = cc.plane("g") < 0.45;
mask.disp();
(foreground * mask).disp();
background = Image.Read("road.png", dtype="float").samesize(foreground)
(background * ~mask).disp();
composite = foreground * mask  + background * ~mask;
composite.disp();
background.choose(foreground, mask).disp();

# Application: Motion detection

video = VideoFile("traffic_sequence.mp4", mono=True, dtype="float")
sigma = 0.02;
background = None
for im in video:
  if background is None:
    background = im  # first frame only
  else:
    d = im - background
    background += d.clip(-sigma, sigma)
  background.disp()

# Spatial Operations


# Linear Spatial Filtering


# Image Smoothing

K = Image.Constant(21, 21, value=1/21**2);
K.shape
mona = Image.Read("monalisa.png", mono=True, dtype="float")
mona.convolve(K).disp();
K = Kernel.Box(h=10);
K = Kernel.Gauss(sigma=5);
mona.convolve(K).disp();
K.shape
mona.smooth(sigma=5).disp();
idisp(K);
span = np.arange(-15, 15 + 1);
X, Y = np.meshgrid(span, span)
plt.subplot(projection="3d").plot_surface(X, Y, K);
K = Kernel.Circle(radius=8, h=15);
K=Kernel.Box(h=1)
np.linalg.matrix_rank(K)
U, s, Vh  = np.linalg.svd(K, full_matrices=True)
Kh = s[0] * U[:, 0]  # 1D horizontal kernel
Kv = Vh[0, :]        # 1D vertical kernel
np.outer(Kh, Kv)

# Border Extrapolation


# Edge Detection

castle = Image.Read("castle.png", mono=True, dtype="float")
profile = castle.image[360, :];
profile.shape
plt.plot(np.diff(profile));
K = [0.5, 0, -0.5];
castle.convolve(K).disp(colormap="signed");
Du = Kernel.Sobel()
castle.convolve(Du).disp(colormap="signed");
castle.convolve(Du.T).disp(colormap="signed");
from scipy.signal import convolve2d
Gu = convolve2d(Du, Kernel.Gauss(sigma=1));
Gu.shape
Iu = castle.convolve(Kernel.DGauss(sigma=2));
Iv = castle.convolve(Kernel.DGauss(sigma=2).T);
m = (Iu ** 2 + Iv ** 2).sqrt()
th = Iv.apply2(Iu, np.arctan2);  # arctan2(Iv, Iu)
plt.quiver(castle.uspan(20), castle.vspan(20),
  Iu.image[::20, ::20], Iv.image[::20, ::20], scale=10);
Iu, Iv = castle.gradients(Kernel.DGauss(sigma=2))
edges = castle.canny()
L = Kernel.Laplace()
lap = castle.convolve(Kernel.LoG(sigma=2));
profile = lap.image[360, 570:601];
plt.plot(np.arange(570, 601), profile, "-o");
zc = lap.zerocross();

# Template Matching

mona = Image.Read("monalisa.png", mono=True, dtype="float");
T = mona.roi([170, 220, 245, 295]);
T.sad(T)
T.ssd(T)
T.ncc(T)
T.sad(T * 0.9)
T.ssd(T * 0.9)
T.ncc(T*0.9)
T.sad(T + 0.1)
T.ssd(T + 0.1)
T.ncc(T + 0.1)
T.zsad(T + 0.1)
T.zssd(T + 0.1)
T.zncc(T + 0.1)
T.zncc(T * 0.9 + 0.1)

# Application: Finding Wally

crowd = Image.Read("wheres-wally.png", mono=True, dtype="float")
crowd.disp();
T = Image.Read("wally.png", mono=True, dtype="float")
T.disp();
sim = crowd.similarity(T, "zncc")
sim.disp(colormap="signed", colorbar=True);
maxima, location = sim.peak2d(scale=2, npeaks=5)
maxima
location
crowd.disp();
plot_circle(centre=location, radius=20, color="k");
plot_point(location, color="none", marker="none", text="  #{}");

# Nonparameteric Local Transforms


# Nonlinear Operations

out = mona.window(np.var, h=3);
mx = mona.rank(rank=0, h=2);
med = mona.rank(rank=11, h=2);
spotty = mona.copy()
pixels = spotty.view1d();  # create a NumPy 1D view
npix = mona.npixels    # total number of pixels
k = np.random.choice(npix, 10_000, replace=True);  # choose 10,000 unique pixels
pixels[k[:5_000]] = 0  # set half of them to zero
pixels[k[5_000:]] = 1  # set half of them to one
spotty.disp();
spotty.rank(rank=4, h=1).disp();
M = np.full((3, 3), True);
M[1, 1] = False
M
max_neighbors = mona.rank(rank=0, footprint=M);
(mona > max_neighbors).disp();

# Mathematical Morphology

im = Image.Read("eg-morph1.png")
im.disp();
S1 = np.ones((5, 5));
e1 = im.morph(S1, op="min")
d1 = e1.morph(S1, op="max")

# Noise Removal

objects = Image.Read("segmentation.png")
objects.disp();
S_circle = Kernel.Circle(3)
closed = objects.close(S_circle);
clean = closed.open(S_circle);
objects.open(S_circle).close(S_circle).disp();

# Boundary Detection

eroded = clean.erode(S_circle)
edge = clean - eroded
edge.disp();

# Hit or Miss Transform

skeleton = clean.thin();
ends = skeleton.endpoint()
joins = skeleton.triplepoint();

# Distance Transform

im = Image.Squares(1, size=256).rotate(0.3).canny()
dx = im.distance_transform(norm="L2")

# Shape Changing


# Cropping

mona.disp();
smile = mona.roi([265, 342, 264, 286])
smile.disp();

# Image Resizing

roof = Image.Read("roof.png", mono=True)
 roof[::7, ::7].disp();
roof.smooth(sigma=3)[::7, ::7].disp();
smaller = roof.scale(1/7, sigma=3)
smaller.replicate(7).disp();

# Image Pyramids

pyramid = mona.pyramid()
len(pyramid)

# Image Warping

Up, Vp = Image.meshgrid(width=500, height=500)
U = 4 * (Up - 100);
V = 4 * (Vp - 200);
p = (300, 200);  # (v, u)
(U[p], V[p])
p = (100, 200);  # (v, u)
(U[p], V[p])
mona.warp(U, V).disp();
M = np.diag([0.25, 0.25, 1]) * SE2(100, 200)
out = mona.affine_warp(M, bgcolor=np.nan);
out.disp(badcolor="r");
S = Twist2.UnitRevolute(mona.centre)
M = S.exp(pi / 6)
out = mona.affine_warp(M, bgcolor=np.nan)
twisted_mona = mona.rotate(pi/6);

# Wrapping Up


# Further Reading


# Sources of Image Data


# Software tools


# Exercises

