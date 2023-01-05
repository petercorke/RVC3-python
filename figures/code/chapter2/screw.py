#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
import pvplus

plotter = pv.Plotter(shape=(2,3), border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.enable_parallel_projection()

screw = pv.read('LeadScrew.stl')
screw.rotate_x(90)
plotter.add_mesh(screw)

plotter.add_axes()

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot='screw.png')
