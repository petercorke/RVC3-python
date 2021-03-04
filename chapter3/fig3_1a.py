import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi

import frames

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()


T = SE3.Rx(90, 'deg').A

print(pv.__version__)


frames.add_frame(plotter, SE3(), color='blue', label='A')
frames.add_frame(plotter, SE3(-2, 0, 0) * SE3.Rz(-pi/2) * SE3.Rx(pi/2), color='red', label='B')

# camera position, focus point, up
# plotter.camera_position = [(2, -2, 1), (0, 0, 0), (0, 0, 1)]

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot='fig3_1a.png')
