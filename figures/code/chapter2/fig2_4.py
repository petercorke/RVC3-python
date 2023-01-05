#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi

import pvplus

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))


box = 0 #1

if box == 0:
    color = 'blue'
    label = 'A'
elif box == 1:
    color = 'red'
    label = 'B'

L = 1.4

# initial box + frame (blue)
pvplus.add_frame(plotter, SE3(), label='A')
cube = pv.Cube(y_length=L, x_length=L/2, z_length=L/2)
plotter.add_mesh(cube, color='blue', show_edges=True, style='wireframe', opacity=0.2, line_width=15)

# final box + frame (red)
T = SE3(-0.5, 1.5, 1.5) * SE3.Rz(pi/4) * SE3.Rx(pi/8) * SE3.Ry(pi/8)
pvplus.add_frame(plotter, T, label='B')
cube = pv.Cube(y_length=L, x_length=L/2, z_length=L/2)
cube.transform(T.A)
plotter.add_mesh(cube, color='red', show_edges=True, style='wireframe', opacity=0.2, line_width=15)

# centre the scene in camera view, look along -X axis
plotter.camera_position = [(2, 1, 1), (0, 1, 1), (0, 0, 1)]

plotter.set_background('white')
plotter.enable_parallel_projection()

# plotter.export_obj('fig2_4')

plotter.show(screenshot='Figures_generated/fig2_4.png')