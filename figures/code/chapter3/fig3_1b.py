#! /usr/bin/env python3

import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi
import pvplus


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()


print(pv.__version__)


dir = [1, 0, 0]
pos = [-1, 0, 0]
plotter.add_mesh(pv.Cylinder(center=pos, direction=dir, radius=0.2, height=2))

# blue frame at the origin
pvplus.add_frame(plotter, SE3(), color='blue', label='A')

# red frame at -2, 0, 0
pvplus.add_frame(plotter, SE3(-2, 0, 0) * SE3.Rz(-pi/2) * SE3.Rx(pi/2), color='red', label='B')

# disk = pv.Cylinder(center=(-2,0,0), direction=(0,1,0), height=0.02, radius=2)
# plotter.add_mesh(disk, color='red', opacity=0.1)


# camera position, focus point, up
# plotter.camera_position = [(2, -2, 1), (0, 0, 0), (0, 0, 1)]

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

pvplus.export_gltf(plotter, 'exported.glb')
plotter.show(screenshot='fig3_1b.png')

