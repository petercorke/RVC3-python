#! /usr/bin/env python3
import pyvista as pv

import numpy as np
# from spatialmath import SE3
from spatialmath import base
from math import cos, sin, pi
import pvplus
import roboticstoolbox as rtb
from rvcprint import outfile

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
print(pv.__version__)

puma = rtb.models.DH.Puma560()

J = puma.jacob0(puma.qn)
M = puma.inertia(puma.qn)
Mi = np.linalg.inv(M)
Mx = J @ Mi @ Mi.T @ J.T

E = Mx[:3, :3]
print(E)

e, _ = np.linalg.eig(E)

# the radii are square root of the eigenvalues
radii = np.sqrt(e)
print(radii)

from spatialmath import base
base.plot_ellipsoid(E, inverted=True)

# clf
# puma.vellipse(qns, 'rot')

pvplus.ellipsoid_3d(plotter, E*10, inverted=True)

# plotter.add_text('boo!', (500, 500))
plotter.set_background('white')

# plotter.show_bounds()

# plotter.add_axes()
# plotter.export_obj('exported.obj')
plotter.show(screenshot=outfile(format='png'))
