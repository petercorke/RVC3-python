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

# robot = rtb.models.DH.Puma560()
robot = rtb.models.URDF.UR5()

J = robot.jacob0(robot.q1)

Jt = J[:3,:]

E = np.linalg.inv(Jt @ Jt.T)
print(E)

e, _ = np.linalg.eig(E)

# the radii are square root of the eigenvalues
radii = 1 / np.sqrt(e)
print(radii)

# from spatialmath import base
# base.plot_ellipsoid(E, inverted=True)

# clf
# puma.vellipse(qns, 'rot')

pvplus.ellipsoid_3d(plotter, E, inverted=False)
plotter.add_axes(line_width=5, color='black')

# plotter.add_text('boo!', (500, 500))
plotter.set_background('white')

# plotter.show_bounds()
plotter.show()

# plotter.add_axes()
# plotter.export_obj('exported.obj')
#plotter.show(screenshot=outfile(format='png'))