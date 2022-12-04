#!/usr/bin/env python3

import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi
from roboticstoolbox import ETS2 as ET

import pvplus

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
overlap = 0.2
r = 100
eer = 0.06
q1 = 0.7
eer = 0.06
opacity = 0.3
wf = True
zl = -0.4

T1 = SE3.Rz(q1)
TE = SE3.Rz(q1) * SE3.Tx(1)


## link 1
L1 = pv.Box(bounds=(-overlap, 1, -0.2, 0.2, -0.05, 0.05))
L1.transform(T1.A)
plotter.add_mesh(L1, color='red', show_edges=wf, opacity=opacity)

pvplus.add_frame2(plotter, SE3(0, 0, zl), scale=0.5, label='O')

# joint
# J1 = pv.Arrow(start=(0, 0, -.4), direction=(0,0,1), tip_resolution=r, 
#     shaft_resolution=r, shaft_radius=0.03, tip_radius=0.08, tip_length=0.2)
pvplus.axis(plotter, text='q')

# end-effector
EE = pv.Sphere(radius=eer, center=(0,0, 0))
EE.transform(TE.A)
pvplus.add_frame2(plotter, TE, scale=0.5, label='E')

plotter.add_mesh(EE, color='black')

# centre the scene in camera view, look along -X axis
plotter.camera_position = [(3,-4, 2), (1, 0, 0), (0, 0, 1)]

plotter.set_background('white')
plotter.disable_parallel_projection()

# plotter.show_axes()  # put a small frame for orientation in bottom left
# plotter.show_bounds(grid='front')  # overlay a grid
pvplus.save(plotter, show=False, zoom=1.2)