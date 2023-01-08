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

from machinevisiontoolbox.base import *
from machinevisiontoolbox import *
from spatialmath.base import *
from spatialmath import SE2, Twist2

# ------------------------------ #

# # 11.1 Obtaining an Image
# ## 11.1.1 Images from Files
#

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

church = Image.Read("church.jpg");
church.metadata()

# ## 11.1.2 Images from File Sequences
#

images = ImageCollection("seq/*.png");
len(images)

images[3]

for image in images:
  image.disp()  # do some operation

# this may fail unless you have installed these extra image zip files
# see https://github.com/petercorke/machinevision-toolbox-python/tree/master/mvtb-data#install-big-image-files
# images = ZipArchive("bridge-l.zip", "*.pgm");
len(images)

# ## 11.1.3 Images from an Attached Camera
#

camera = VideoCamera(0)

image = camera.grab()

camera.release()


# ## 11.1.4 Images from a Video File
#

video = VideoFile("traffic_sequence.mp4")

video.shape

for frame in video:
  frame.disp(fps=video.fps) # display frame in the same axes

# ## 11.1.5 Images from the Web
#

dartmouth = WebCam("https://webcam.dartmouth.edu/webcam/image.jpg");

dartmouth.grab().disp();

# ## 11.1.6 Images from Space
#

world = EarthView();

world.grab(-27.475722, 153.0285, 17).disp();

world.grab(-27.475722,153.0285, 15, type="map").disp();

world.grab(-27.475722,153.0285, 15, type="roads").disp();

# ## 11.1.7 Images from Code
#

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


#  11.2 Pixel Value Distribution
#
plt.close('all')
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

# # 11.3 Monadic Operations
#

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

church.apply(lambda x: x // 64, vectorize=True).disp()

church.npixels

church.apply(lambda x: x // 64).disp();

lut = [x // 64 for x in range(256)];  # create posterization lookup table
church.LUT(lut).disp();

# # 11.4 Dyadic Operations
#

church / 2       # new Image with all pixel values halved
church + 20      # new Image with all pixel values increased by 20
church - church  # new Image with all pixel values equal to 0

church.apply2(church, lambda x, y: x - y, vectorize=True).disp()

church.apply2(church, lambda x, y: x - y).disp();

a = np.uint8(100)
b = np.uint8(200)

a + b
a - b

-a

a / b

# ## 11.4.1 Applications
# ### 11.4.1.1 Application: Chroma Keying
#

foreground = Image.Read("greenscreen.png", dtype="float")

cc = foreground.gamma_decode("sRGB").chromaticity()

cc.plane("g").hist().plot()

mask = cc.plane("g") < 0.45;
mask.disp();

(foreground * mask).disp();

background = Image.Read("road.png", dtype="float").samesize(foreground)

(background * ~mask).disp();

composite = foreground * mask  + background * ~mask;
composite.disp();

background.choose(foreground, mask).disp();

# ### 11.4.1.2 Application: Motion detection
#

video = VideoFile("traffic_sequence.mp4", mono=True, dtype="float")

sigma = 0.02;
background = None
for im in video:
  if background is None:
    background = im  # first frame only
  else:
    d = im - background
    background += d.clip(-sigma, sigma)
  background.disp(fps=video.fps)

# # 11.5 Spatial Operations
# ## 11.5.1 Linear Spatial Filtering
#

# O = I.convolve(K);

# ### 11.5.1.1 Image Smoothing
#
plt.close('all')

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

# ### 11.5.1.2 Border Extrapolation
# ### 11.5.1.3 Edge Detection
#

plt.clf()

castle = Image.Read("castle.png", mono=True, dtype="float")

profile = castle.image[360, :];
profile.shape

plt.plot(profile);

plt.plot(np.diff(profile));

K = [0.5, 0, -0.5];
castle.convolve(K).disp(colormap="signed");

Du = Kernel.Sobel()

castle.convolve(Du).disp(colormap="signed");

castle.convolve(Du.T).disp(colormap="signed");

from scipy.signal import convolve2d
Gu = convolve2d(Du, Kernel.Gauss(sigma=1));
Gu.shape

Xu = castle.convolve(Kernel.DGauss(sigma=2));
Xv = castle.convolve(Kernel.DGauss(sigma=2).T);

m = (Xu ** 2 + Xv ** 2).sqrt()

th = Xv.apply2(Xu, np.arctan2);  # arctan2(Xv, Xu)

plt.quiver(castle.uspan(20), castle.vspan(20),
  Xu.image[::20, ::20], Xv.image[::20, ::20], scale=10);

Xu, Xv = castle.gradients(Kernel.DGauss(sigma=2))

edges = castle.canny()

L = Kernel.Laplace()

lap = castle.convolve(Kernel.LoG(sigma=2));

profile = lap.image[360, 570:601];
plt.plot(np.arange(570, 601), profile, "-o");

zc = lap.zerocross();

# ## 11.5.2 Template Matching
#

mona = Image.Read("monalisa.png", mono=True, dtype="float");
A = mona.roi([170, 220, 245, 295]);

B = A
A.sad(B)
A.ssd(B)
A.ncc(B)

B = 0.9 * A
A.sad(B)
A.ssd(B)

A.ncc(B)

B = A + 0.1
A.sad(B)
A.ssd(B)
A.ncc(B)

A.zsad(B)
A.zssd(B)
A.zncc(B)

B = 0.9 * A + 0.1
A.zncc(B)

# ### 11.5.2.1 Application: Finding Wally
#

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

# ### 11.5.2.2 Nonparameteric Local Transforms
# ## 11.5.3 Nonlinear Operations
#

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

# # 11.6 Mathematical Morphology
#

im = Image.Read("eg-morph1.png")
im.disp();

S = np.ones((5, 5));

e1 = im.morph(S, op="min")

# morphdemo(im, S, op="min")

d1 = e1.morph(S, op="max")

out = im.erode(S);
out = im.dilate(S);

# ## 11.6.1 Noise Removal
#

objects = Image.Read("segmentation.png")
objects.disp();

S_circle = Kernel.Circle(3)

closed = objects.close(S_circle);

clean = closed.open(S_circle);

objects.open(S_circle).close(S_circle).disp();

# ## 11.6.2 Boundary Detection
#

eroded = clean.erode(S_circle)

edge = clean - eroded
edge.disp();

# ## 11.6.3 Hit or Miss Transform
#

# out = image.hitormiss(S);

skeleton = clean.thin();

ends = skeleton.endpoint()

joins = skeleton.triplepoint();

# ## 11.6.4 Distance Transform
#

im = Image.Squares(1, size=256).rotate(0.3).canny()

dx = im.distance_transform(norm="L2")

# # 11.7 Shape Changing
# ## 11.7.1 Cropping
#

plt.close('all')

mona.disp();

# Select a region of interest on the image, left click then drag
# eyes, roi = mona.roi();
#eyes

#roi

smile = mona.roi([265, 342, 264, 286])
smile.disp();

# ## 11.7.2 Image Resizing
#

roof = Image.Read("roof.png", mono=True)

roof[::7, ::7].disp();

roof.smooth(sigma=3)[::7, ::7].disp();

smaller = roof.scale(1/7, sigma=3)

smaller.replicate(7).disp();

# ## 11.7.3 Image Pyramids
#

pyramid = mona.pyramid()
len(pyramid)

# ## 11.7.4 Image Warping
#

Up, Vp = Image.meshgrid(width=500, height=500)

U = 4 * (Up - 100);
V = 4 * (Vp - 200);

p = (300, 200);  # (v, u)
(U[p], V[p])

p = (100, 200);  # (v, u)
(U[p], V[p])

mona.warp(U, V).disp();

M = np.diag([0.25, 0.25, 1]) * SE2(100, 200) 

out = mona.warp_affine(M, bgcolor=np.nan);
out.disp(badcolor="r");

S = Twist2.UnitRevolute(mona.centre)

M = S.exp(pi / 6)
out = mona.warp_affine(M, bgcolor=np.nan)

twisted_mona = mona.rotate(pi/6);
twisted_mona.disp()


