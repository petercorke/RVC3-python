#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import pi
import pvplus
import rvcprint

plotter = pv.Plotter(border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.set_background('white')
plotter.enable_parallel_projection()

print(pv.__version__)


def add_plot(i, j, T):
	print(i, j, T)
	pvplus.add_frame(plotter, T)

acolor = '#e0e0e0'
Rx = SE3().Rx(90, 'deg')
Ry = SE3().Ry(90, 'deg')


## top row

add_plot(0, 0, SE3())
rib = pvplus.ribbon(phase=0, T= SE3(0.5, 0, 0) * SE3.Ry(-pi/2))
plotter.add_mesh(rib, color=acolor)

# doesn't support Unicode greek letters or mathtext, seems to be a VTK/Python issue
# plotter.add_point_labels(np.r_[0.5, 0, -0.5], ["$\pi/2$"], fill_shape=False, text_color='black', font_size=32)

add_plot(0, 1, SE3.Ty(2.5) * Rx)
rib = pvplus.ribbon(phase=-0.18, T= SE3.Ty(2.5) * Rx * SE3(0, 0.45, 0) * SE3.Rx(pi/2))
plotter.add_mesh(rib, color=acolor)
print('--------')
print(plotter.camera_position)
print(plotter.camera)

add_plot(0, 2, SE3.Ty(3.5) * Rx * Ry)

plotter.export_gltf('fig2_16a.gltf')

## bottom row
plotter = pv.Plotter(border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.set_background('white')
plotter.enable_parallel_projection()

add_plot(1, 0, SE3())
rib = pvplus.ribbon(phase=0, T= SE3(0, 0.5, 0) * SE3.Rx(pi/2))
plotter.add_mesh(rib, color='gray')

add_plot(1, 1, SE3.Ty(1.5) * Ry)
rib = pvplus.ribbon(phase=0.05, T= SE3.Ty(1.5) * Ry * SE3(0.42, 0, 0) * SE3.Ry(-pi/2))
plotter.add_mesh(rib, color=acolor)

add_plot(1, 2, SE3.Ty(4) * Ry * Rx)

plotter.export_gltf('fig2_16b.gltf')
