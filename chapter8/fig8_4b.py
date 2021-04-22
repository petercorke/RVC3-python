import pyvista as pv
import vtk

import numpy as np
# from spatialmath import SE3
from spatialmath import base
from math import cos, sin, pi
import pvplus
import roboticstoolbox as rtb


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
puma = rtb.models.DH.Puma560()
qns = puma.qr
qns[4] = np.deg2rad(5)
J = puma.jacob0(qns)


Jt = J[3:,:]

E = Jt @ Jt.T
print(E)

# clf
# puma.vellipse(qns, 'rot')

pvplus.ellipsoid_3d(plotter, E, inverted=True)

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots
# plotter.add_axes()
# plotter.export_obj('exported.obj')
plotter.show(screenshot='fig8_4b.png')