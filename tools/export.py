import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi
import frames

# colors = ['red', 'green', 'blue']
# plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
# plotter.enable_parallel_projection()

# T = SE3().A

# a1 = frames.add_arrow(plotter, T, 0, color=colors[0])
# a2 = frames.add_arrow(plotter, T, 1, color=colors[1])
# a3 = frames.add_arrow(plotter, T, 2, color=colors[2])

# frame = a1 + a2 + a3
# # frame.save('exported.ply')  # ply, vtk, stk
# pv.save_meshio('exported.ply', frame, binary=False)
