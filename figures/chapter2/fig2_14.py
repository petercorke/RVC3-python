#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi
import pvplus
import rvcprint


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000), off_screen=True)
# plotter.enable_parallel_projection()
plotter.disable_parallel_projection()

pvplus.add_frame(plotter, SE3(), color='blue', label='A')
pvplus.add_frame(plotter, SE3(-.4,1.5,.8) * SE3.OA([0.5,1,.6], [-.3,.7,.7]), 
    color='red', label='B')

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

filename = rvcprint.outfile(format='png', include=True)

plotter.show(screenshot=filename)
