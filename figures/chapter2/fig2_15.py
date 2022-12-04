#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
import pvplus
import rvcprint

plotter = pv.Plotter(shape=(2,3), border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.enable_parallel_projection()

def add_plot(i, j, T):
	print(i, j, T)
	plotter.subplot(i, j)
	pvplus.add_frame(plotter, T)


add_plot(0, 0, SE3())
add_plot(0, 1, SE3().Rx(90, 'deg'))
add_plot(0, 2, SE3().Rx(180, 'deg'))
add_plot(1, 0, SE3().Rx(-90, 'deg'))
add_plot(1, 1, SE3().Ry(90, 'deg'))
add_plot(1, 2, SE3().Rz(90, 'deg'))


plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot=rvcprint.outfile(format='png'))