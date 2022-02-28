#! /usr/bin/env python3

import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi
import pvplus


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()


# blue frame at the origin
pvplus.add_frame(plotter, SE3.RPY([0.2, 0.3, 0.4]), color='gray')

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot='fig3_1c.png')

