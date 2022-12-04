#!/usr/bin/env python3

from roboticstoolbox import *
import pyvista as pv
import pvplus

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))

# link1 = path_to_datafile("xacro/franka_description/meshes/visual/link1.dae")
# print(link1)

mesh = pv.read("link1.ply")
mesh.points *= 20
plotter.add_mesh(mesh, color='gray', opacity=0.3, show_edges=True)

pvplus.add_frame(plotter, None, scale=1, label='1')

plotter.set_background('white')

# centre the scene in camera view, look along -X axis
plotter.camera_position = [(12, 12, -1), (0, 0, 0), (0, 1, 0.5)]

# plotter.save_graphic('fig7_6.svg', raster=False)
pvplus.save(plotter)