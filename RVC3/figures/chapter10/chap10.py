#!/usr/bin/env python3

## RVC2: Chapter 10 - Light and Color
from machinevisiontoolbox.base.color import plot_chromaticity_diagram, plot_spectral_locus
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9
um = 1e-6

## 10.1  Spectral representation of light

λ = np.arange(300, 1_001, 10) * nm;

for T in np.arange(3_000, 6_001, 1_000):
    plt.plot(λ, blackbody(λ, T))

# %%

lamp = blackbody(λ, 2_600);
sun = blackbody(λ, 5_778);
plt.plot(λ / nm, np.c_[lamp / np.max(lamp), sun / np.max(sun)])

## 10.1.1  Absorption

sun_ground = loadspectrum(λ, 'solar');
plt.plot(λ, sun_ground)

λ = np.arange(400, 701) * nm;
A = loadspectrum(λ, 'water');
d = 5;
T = 10 ** (-A * d);
plt.plot(λ, T)

## 10.1.2  Reflectance

λ = np.arange(100, 10_001, 10) * nm;
R = loadspectrum(λ, 'redbrick');
plt.plot(λ / um, R)

## 10.1.3  Luminance

λ = np.arange(400, 701) * nm;

E = loadspectrum(λ, 'solar');

R = loadspectrum(λ, 'redbrick');

L = E * R;
plt.plot(λ / nm, L);

## 10.2  Color

human = luminos(λ);
plt.plot(λ,  human)

luminos(450 * nm) / luminos(550 * nm)

## 10.2.1  The human eye

cones = loadspectrum(λ, 'cones');
plt.plot(λ, cones)

## 10.2.2  Measuring color

np.sum(np.c_[L, L, L] * cones * nm, axis=0)

## 10.2.3  Reproducing colors

λ = np.arange(400, 701) * nm;
cmf = cmfrgb(λ);
plt.plot(λ, cmf)

green = cmfrgb(500 * nm)

white = -np.min(green) * np.r_[1, 1, 1]

feasible_green = green + white

RGB_brick = cmfrgb(λ, L)


## 10.2.4  Chromaticity space

plt.clf()

rg = lambda2rg(np.arange(400, 701) * nm);
plt.plot(rg[:, 0], rg[:, 1])

plot_spectral_locus('rg')

primaries = lambda2rg(cie_primaries())
plot_point(primaries.T, 'o')

green_cc = lambda2rg(500 * nm)
plot_point(green_cc, '*')

white_cc = tristim2cc([1, 1, 1])
plot_point(white_cc, 'H')

plt.clf()
cmf = cmfxyz(λ);
plt.plot(λ, cmf);

plt.clf()
xy = lambda2xy(λ);
plt.plot(xy[0], xy[1], 'ko')

plt.clf()
plot_chromaticity_diagram('xy')

lambda2xy(550 * nm)

lamp = blackbody(λ, 2_601);
lambda2xy(λ, lamp)

## 10.2.5  Color names

colorname('?burnt')

colorname('burntsienna')

bs = colorname('burntsienna', 'xy')

colorname('chocolate', 'xy')

colorname([0.2, 0.3, 0.4])

## 10.2.6  Other color and chromaticity spaces

colorspace_convert([1, 0, 0], 'RGB', 'HSV')
colorspace_convert([0, 1, 0], 'RGB', 'HSV')
colorspace_convert([0, 0, 1], 'RGB', 'HSV')

colorspace_convert([0, 0.5, 0], 'RGB', 'HSV')

colorspace_convert([0.4, 0.4, 0.4], 'RGB', 'HSV')

colorspace_convert(np.r_[0, 0.5, 0] + np.r_[0.4, 0.4, 0.4], 'RGB', 'HSV')

flowers = Image.Read('flowers4.png')

hsv = flowers.colorspace('HSV')

hsv.plane('H').disp()
hsv.plane('S').disp()
hsv.plane('V').disp()


Lab = flowers.colorspace('Lab')

Lab.plane('a').disp()
Lab.plane('b').disp()


## 10.2.7  Transforming between different primaries

C = np.array([
        [0.7347,  0.2738, 0.1666],
        [0.2653,  0.7174, 0.0088],
        [0,       0.0089, 0.8245]
             ])

white = np.r_[0.3127, 0.3290, 0.3582];
J = np.linalg.inv(C) @  white / white[1]
C @ np.diag(J)

XYZ_brick = C @ np.diag(J) @ RGB_brick.T

tri = tristim2cc(XYZ_brick.T)
colorname(tri, 'xy')

## 10.2.8  What is white?

d65 = blackbody(λ, 6500);
lambda2xy(λ, d65)

ee = np.ones(λ.shape);

lambda2xy(λ, ee)

## 10.3.2  Color constancy

λ = np.arange(400, 701) * nm;
R = loadspectrum(λ, 'redbrick');

sun = loadspectrum(λ, 'solar');

lamp = blackbody(λ, 2_600);

xy_sun = lambda2xy(λ, sun * R)
xy_lamp = lambda2xy(λ, lamp * R)


## 10.3.4  Color change due to absorption

λ = np.arange(400, 701) * nm;

R = loadspectrum(λ, 'redbrick.dat');
sun = loadspectrum(λ, 'solar.dat');
A = loadspectrum(λ, 'water.dat');

d = 2;

T = 10.0 ** (-d * A);

L = sun * R * T;

xy_water = lambda2xy(λ, L)


## 10.3.6  Gamma


wedge = np.arange(0, 1.05, 0.1).reshape(1,-1);
Image(wedge).disp()
Image(wedge ** (1 / 2.2)).disp()
## 10.4.1  Comparing color spaces

λ = np.arange(400, 701) * nm;
macbeth = loadspectrum(λ, 'macbeth.dat');

d65 = loadspectrum(λ, 'D65') * 3e9;

λ = np.arange(400, 701) * nm;
XYZ = np.empty((24, 3));
Lab = np.empty((24, 3));
for i in range(24):
    L = macbeth[:,i] * d65;
    tristim = np.maximum( cmfrgb(λ, L), 0);
    RGB = tristim.reshape((1, 1, 3)).astype(np.float32);
    XYZ[i,:] = colorspace_convert(RGB, 'rgb', 'xyz');
    Lab[i,:] = colorspace_convert(RGB, 'rgb', 'lab');

# xy = XYZ[:, :2] / np.tile(np.sum(XYZ, axis=1), (2,1)).T
xy = tristim2cc(XYZ)
ab = Lab[:, 1:];

plot_chromaticity_diagram('xy')
plot_point(xy.T, marker='k*', text=' {:d}', fontsize=8)

## 10.4.2  Shadow removal

im = Image.Read('parks.png', gamma='sRGB', dtype='float')
gs = shadow_invariant(im.image, 0.7)
Image(gs).disp(interpolation='none', badcolor='red')
