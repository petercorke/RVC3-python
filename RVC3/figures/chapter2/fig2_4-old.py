#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
ss = False
se = False
r = 100
th = 0.3
s=0.8
sp=10
colors = [(0.5,0,0), '#c0c20a', 'blue']


T = SE3.Rx(90, 'deg').A

print(pv.__version__)


def add_arrow(p, i, T, opacity=1.0):

	pos = [0, 0, 0]
	pos[i] = 1.1

	arrow = pv.Arrow(direction=pos, tip_resolution=r, shaft_resolution=r)
	arrow.transform(T)
	p.add_mesh(arrow, color=colors[i], specular=s, specular_power=sp, smooth_shading=ss, show_edges=se, opacity=opacity)

	names = 'XYZ'

	text = pv.Text3D(names[i], depth=th)

	text.points -= np.mean(text.points, axis=0)
	text.points /= 5
	if i == 0:
		text.rotate_x(-90)
	elif i == 1:
		text.rotate_y(90)
		text.rotate_x(90)
	elif i == 2:
		text.rotate_x(-90)

	text.translate(pos)
	text.transform(T)
	p.add_mesh(text, color=colors[i], opacity=opacity)

def add_plot(T, opacity=1.0):

	T = T.A
	add_arrow(plotter, 0, T, opacity=opacity)
	add_arrow(plotter, 1, T, opacity=opacity)
	add_arrow(plotter, 2, T, opacity=opacity)
	plotter.enable_parallel_projection()


add_plot(SE3(), opacity=0.1)
add_plot(SE3([-0.3,.6,.4]))

plotter.set_background('white')
plotter.disable_parallel_projection()
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.show(screenshot='axes.png')