#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import pi
import pvplus
import rvcprint

plotter = pv.Plotter(shape=(2,3), border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.set_background('white')
plotter.enable_parallel_projection()

print(pv.__version__)


def add_plot(i, j, T):
	print(i, j, T)
	plotter.subplot(i, j)
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

add_plot(0, 1, Rx)
rib = pvplus.ribbon(phase=-0.18, T= Rx * SE3(0, 0.45, 0) * SE3.Rx(pi/2))
plotter.add_mesh(rib, color=acolor)
print('--------')
print(plotter.camera_position)
print(plotter.camera)

add_plot(0, 2, Rx * Ry)


## bottom row
add_plot(1, 0, SE3())
rib = pvplus.ribbon(phase=0, T= SE3(0, 0.5, 0) * SE3.Rx(pi/2))
plotter.add_mesh(rib, color='gray')
plotter.add_text('original pose', position='lower_edge', color='black')

add_plot(1, 1, Ry)
rib = pvplus.ribbon(phase=0.05, T= Ry * SE3(0.42, 0, 0) * SE3.Ry(-pi/2))
plotter.add_mesh(rib, color=acolor)
plotter.add_text('after first rotation', position='lower_edge', color='black')

add_plot(1, 2, Ry * Rx)
plotter.add_text('after second rotation', position='lower_edge', color='black')



# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot=rvcprint.outfile(format='png'))