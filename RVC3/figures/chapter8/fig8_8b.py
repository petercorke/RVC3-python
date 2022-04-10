#! /usr/bin/env python3
import pyvista as pv
import vtk

import numpy as np
# from spatialmath import SE3
from spatialmath import base
from math import cos, sin, pi
import pvplus
import roboticstoolbox as rtb
from rvcprint import outfile


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.disable_parallel_projection()
print(pv.__version__)

# from https://github.com/pyvista/pyvista/issues/952

E = np.array([
        [ 0.0076,    0.0000,   -0.0868],
        [ 0.0000,    3.0000,   -0.0000],
        [-0.0868,   -0.0000,    2.9924]
    ])

print(E)

# robot = rtb.models.DH.Puma560()
robot = rtb.models.URDF.UR5()
qns =  np.full((6,), np.deg2rad(1))
J = robot.jacob0(qns)


Jt = J[3:,:]

E = np.linalg.inv(Jt @ Jt.T)
print(E)
e, _ = np.linalg.eig(E)

radii = 1 / np.sqrt(e)
print(radii)


# clf
# puma.vellipse(qns, 'rot')

pvplus.ellipsoid_3d(plotter, E, inverted=False)
plotter.add_axes(line_width=5, color='black')

plotter.set_background('white')
plotter.show()
# plotter.enable_eye_dome_lighting()  # messes up subplots
# plotter.add_axes()
# plotter.export_obj('exported.obj')
# plotter.show(screenshot=outfile(format='png'))