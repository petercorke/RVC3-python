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
from machinevisiontoolbox import Image
from spatialmath.base import *

# ------------------------------ #

# # 10.1 Spectral Representation of Light
#

nm = 1e-9;
lmbda = np.linspace(300, 1_000, 100) * nm;

for T in np.arange(3_000, 6_001, 1_000):
  plt.plot(lmbda, blackbody(lmbda, T))

lamp = blackbody(lmbda, 2_600);
sun = blackbody(lmbda, 5_778);
plt.plot(lmbda / nm, np.c_[lamp / np.max(lamp), sun / np.max(sun)]);

# ## 10.1.1 Absorption
#

sun_ground = loadspectrum(lmbda, "solar");
plt.plot(lmbda, sun_ground);

lmbda = np.linspace(300, 1_000, 100) * nm;
A = loadspectrum(lmbda, "water");

d = 5;
T = 10 ** (-A * d);
plt.plot(lmbda, T);

# ## 10.1.2 Reflectance
#

lmbda = np.linspace(100, 10_000, 100) * nm;
R = loadspectrum(lmbda, "redbrick");
plt.plot(lmbda / (1_000 * nm), R);

# ## 10.1.3 Luminance
#

lmbda = np.arange(400, 701) * nm;
E = loadspectrum(lmbda, "solar");

R = loadspectrum(lmbda, "redbrick");

L = E * R;
plt.plot(lmbda / nm, L);

# # 10.2 Color
# ## 10.2.1 The Human Eye
#

cones = loadspectrum(lmbda, "cones");
plt.plot(lmbda, cones);

# ### 10.2.1.1 Perceived Brightness
#

human = luminos(lmbda);
plt.plot(lmbda,  human);

luminos(450 * nm) / luminos(550 * nm)

# ## 10.2.2 Camera sensor
# ## 10.2.3 Measuring Color
#

np.sum(np.c_[L, L, L] * cones * nm, axis=0)

# ## 10.2.4 Reproducing Colors
#

cmf = cmfrgb(lmbda);
plt.plot(lmbda, cmf);

green = cmfrgb(500 * nm)

w = -np.min(green)
feasible_green = green + w

RGB_brick = cmfrgb(lmbda, L)

# ## 10.2.5 Chromaticity Coordinates
#

rg = lambda2rg(np.linspace(400, 700, 100) * nm);
plt.plot(rg[:, 0], rg[:, 1]);

plot_spectral_locus("rg")

primaries = lambda2rg(cie_primaries()).T

plot_point(primaries, "o");

green_cc = lambda2rg(500 * nm)
plot_point(green_cc, "x");

white_cc = tristim2cc([1, 1, 1])
plot_point(white_cc, "o");

cmf = cmfxyz(lmbda);
plt.plot(lmbda, cmf);

xy = lambda2xy(lmbda);
plt.plot(xy[0], xy[1], "ko");

plot_chromaticity_diagram("xy")

lambda2xy(550 * nm)

lamp = blackbody(lmbda, 2_600);
lambda2xy(lmbda, lamp)

# ## 10.2.6 Color Names
#

name2color("orange")

bs = name2color("orange", "xy")

name2color(".*coral.*")

color2name([0.45, 0.48], "xy")

# ## 10.2.7 Other Color and Chromaticity Spaces
#

colorspace_convert([1, 0, 0], "RGB", "HSV")
colorspace_convert([0, 1, 0], "RGB", "HSV")
colorspace_convert([0, 0, 1], "RGB", "HSV")

colorspace_convert([0, 0.5, 0], "RGB", "HSV")

colorspace_convert([0.4, 0.4, 0.4], "RGB", "HSV")

colorspace_convert(np.array([0, 0.5, 0]) + np.array([0.4, 0.4, 0.4]), "RGB", "HSV")

flowers = Image.Read("flowers4.png")

hsv = flowers.colorspace("HSV")

hsv.plane("H").disp();
hsv.plane("S").disp();
hsv.plane("V").disp();

Lab = flowers.colorspace("L*a*b*")

Lab.plane("a*:").disp();
Lab.plane("b*:").disp();

# ## 10.2.8 Transforming between Different Primaries
#

C = np.array([
    [0.7347,  0.2738, 0.1666],
    [0.2653,  0.7174, 0.0088],
    [0,       0.0089, 0.8245]]);

white = np.array([0.3127, 0.3290, 0.3582]);
J = np.linalg.inv(C) @  white / white[1]
C @ np.diag(J)

XYZ_brick = (C @ np.diag(J) @ RGB_brick).T

tri = tristim2cc(XYZ_brick)

color2name(tri, "xy")

## 10.2.9 What Is White?
d65 = blackbody(lmbda, 6_500);
lambda2xy(lmbda, d65)

ee = np.ones(lmbda.shape);

lambda2xy(lmbda, ee)

# # 10.3 Advanced Topics
# ## 10.3.2 Color Constancy
#

lmbda = np.arange(400, 701) * nm;
R = loadspectrum(lmbda, "redbrick");

sun = loadspectrum(lmbda, "solar");

lamp = blackbody(lmbda, 2_600);

xy_sun = lambda2xy(lmbda, sun * R)
xy_lamp = lambda2xy(lmbda, lamp * R)

# ## 10.3.4 Color Change Due to Absorption
#

lmbda = np.arange(400, 701) * nm;
R = loadspectrum(lmbda, "redbrick");

sun = loadspectrum(lmbda, "solar");

A = loadspectrum(lmbda, "water");

d = 2;

T = 10.0 ** (-d * A);

L = sun * R * T;

xy_water = lambda2xy(lmbda, L)

# ## 10.3.6 Gamma
#

wedge = np.linspace(0, 1, 11).reshape(1,-1);
Image(wedge).disp();

Image(wedge ** (1 / 2.2)).disp();

# # 10.4 Application: Color Images
# ## 10.4.1 Comparing Color Spaces
#

lmbda = np.linspace(400, 700, 100) * nm;
macbeth = loadspectrum(lmbda, "macbeth");

d65 = loadspectrum(lmbda, "D65") * 3e9;

XYZ = np.empty((18, 3));
Lab = np.empty((18, 3));
for i in range(18):
  L = macbeth[:,i] * d65;
  tristim = np.maximum(cmfrgb(lmbda, L), 0);
  RGB = tristim.reshape((1, 1, 3)).astype(np.float32);
  XYZ[i,:] = colorspace_convert(RGB, "rgb", "xyz");
  Lab[i,:] = colorspace_convert(RGB, "rgb", "L*a*b*");

xy = tristim2cc(XYZ);
ab = Lab[:, 1:];
xy.shape, ab.shape

plot_chromaticity_diagram("xy")

# ## 10.4.2 Shadow Removal
#

im = Image.Read("parks.png", gamma="sRGB", dtype="float")
s = shadow_invariant(im.image, 0.7);
Image(s).disp(interpolation="none", badcolor="red");

# theta = esttheta(im)

