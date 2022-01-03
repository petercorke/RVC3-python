#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from scipy import interpolate
import matplotlib.path as mpath
import spatialmath.base as base




_white = {
    'd65': [0.3127, 0.3290],  #D65 2 deg
    'e':   [0.33333, 0.33333]  # E
}

_xy_primaries = {
    'itu-709': np.array([
        [0.64, 0.33],
        [0.30, 0.60],
        [0.15, 0.06]]),
    'cie': np.array([
        [0.6400, 0.3300], 
        [0.3000, 0.6000], 
        [0.1500, 0.0600]]),
    'srgb': np.array([
        [0.6400, 0.3300], 
        [0.3000, 0.6000],
        [0.1500, 0.0600]])
}

def XYZ2RGBxform(white='D65', primaries='sRGB'):
    
    if isinstance(white, str):
        try:
            white = _white[white.lower()]
        except:
            raise ValueError('unknown white value, must be one of'
                ', '.join(_white.keys()))
    else:
        white = base.getvector(white, 2)

    if isinstance(primaries, str):
        try:
            primaries = _xy_primaries[primaries.lower()]
        except:
            raise ValueError('unknown primary value, must be one of'
                ', '.join(_xy_primaries.keys()))
    else:
        white = base.getmatrix(primaries, (3,2))

    def column(primaries, i):
        primaries = base.getmatrix(primaries, (None, 2))
        return np.array([
            primaries[i,0] / primaries[i,1],
            1,
            (1 - primaries[i,0] - primaries[i,1]) / primaries[i,1]
        ])

    # build the columns of the inverse transform
    Xr = column(primaries, 0)
    Xg = column(primaries, 1)
    Xb = column(primaries, 2)
    M = np.array([Xr, Xg, Xb]).T

    # determine the white point
    Xw = column(white, 0)
    J = np.linalg.inv(M) @ Xw
    M = np.array([Xr, Xg, Xb]).T @ np.diag(J)

    return M

def xy_chromaticity_diagram(N = 500, Y=1):
    ex = 0.8
    ey = 0.9
    e0 = 0.0

    Nx = round(N * (ex - e0))
    Ny = round(N * (ey - e0))
    # generate colors in xyY color space
    x, y = np.meshgrid(np.linspace(e0, ex, Nx), np.linspace(e0, ey, Ny))
    # hack to prevent divide by zero errors
    y[0,:] = 1e-3

    # convert xyY to XYZ
    Y = np.ones((Ny, Nx)) * Y
    X = Y * x / y
    Z = Y * (1.0 - x - y) /  y
    XYZ = np.dstack((X, Y, Z)).astype(np.float32)

    RGB = colorspace_convert(XYZ, 'xyz', 'rgb')
    mn = np.minimum(np.amin(RGB, axis=2), 0)
    RGB = RGB - mn[..., np.newaxis]
    mx = np.maximum(np.amax(RGB, axis=2), 1)
    RGB = RGB / mx[..., np.newaxis]

    # clip and gamma encode
    RGB = gamma_encode(np.clip(RGB, 0, 1)) 

    # define the spectral locus boundary as xy points, Mx2 matrix
    nm = 1e-9
    λ = np.arange(400, 700, step=5) * nm
    xyz = ccxyz(λ)
    xy_locus = xyz[:, :2]

    ## make a smooth boundary with spline interpolation

    # set up interpolators for x and y
    M = xy_locus.shape[0]
    drange = np.arange(M)
    fxi = interpolate.interp1d(drange, xy_locus[:, 0], kind='cubic')
    fyi = interpolate.interp1d(drange, xy_locus[:, 1], kind='cubic')

    # interpolate in steps of 0.1 
    irange = np.arange(0, M - 1, step=0.1)
    xi = fxi(irange)
    yi = fyi(irange)

    # close the path
    xi = np.append(xi, xi[0])
    yi = np.append(yi, yi[0])

    ## determine which points from xx, yy, are contained within polygon
    ## defined by xi, yi

    # create a polygon
    p = np.stack((xi, yi), axis=-1)
    polypath = mpath.Path(p)

    # flatten x/y grids into array columnwise
    xc = x.flatten('F')
    yc = y.flatten('F')

    # check if these xy points are contained in the polygon
    # returns a bool array
    pts_in = polypath.contains_points(np.stack((xc, yc), axis=-1))
    # reshape it to size of original grids
    outside = np.reshape(~pts_in, x.shape, 'F')

    # set outside pixels to white
    outside3 = np.dstack((outside, outside, outside))
    RGB[outside3] = 1.0

    return np.flip(RGB, axis=0)  # flip top to bottom

def ab_chromaticity_diagram(L=100, N=256):
    a, b = np.meshgrid(np.linspace(-128, 127, N), np.linspace(-128, 127, N))

    # convert from Lab to RGB
    ac = a.flatten('F')
    bc = b.flatten('F')

    L = np.ones(a.shape) * L
    Lab = np.dstack((L, a, b)).astype(np.float32)

    # TODO currently does not work. OpenCV
    # out = cv.cvtColor(Lab, cv.COLOR_Lab2BGR)

    RGB = colorspace_convert(Lab, 'lab', 'rgb')
    mn = np.minimum(np.amin(RGB, axis=2), 0)
    RGB = RGB - mn[..., np.newaxis]
    mx = np.maximum(np.amax(RGB, axis=2), 1)
    RGB = RGB / mx[..., np.newaxis]

    # probably should gamma encode but it looks bad
    RGB = gamma_encode(np.clip(RGB, 0, 1))

    outside = np.sqrt(a**2 + b**2) > 128
    # set outside pixels to white
    outside3 = np.dstack((outside, outside, outside))
    RGB[outside3] = 1.0

    return np.flip(RGB, axis=0)  # flip top to bottom

def plot_chromaticity_diagram(colorspace='xy', brightness=1, alpha=1):

    if colorspace in ('XY', 'xy'):
        RGB = xy_chromaticity_diagram(Y=brightness)
        plt.imshow(RGB, extent=(0,0.8, 0, 0.9), alpha=alpha)
        plt.xlabel('x')
        plt.ylabel('y')
    elif colorspace in ('Lab', 'lab', 'ab'):
        RGB = ab_chromaticity_diagram(L=brightness*100)
        plt.imshow(RGB, extent=(-128, 127, -128, 127), alpha=alpha)
        plt.xlabel('a*')
        plt.ylabel('b*')

    plt.show(block=True)

# plot_xy_chromaticity_diagram()
# ab_chromaticity_diagram()

# plot_chromaticity_diagram('xy', brightness=1)

from matplotlib import cm

a = np.zeros((5, 5))
a[2,2] = -1
a[3,3] = np.inf
a[4,4] = np.nan

# cmap = cm.get_cmap('gray', 256)
# cmap.set_under(color='red')
# cmap.set_over(color='blue')
# cmap.set_bad(color='yellow')
# plt.imshow(a, vmin=0, vmax=1, cmap=cmap)

Image(a).disp()

plt.show(block=True)
