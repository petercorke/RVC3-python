import pyvista as pv
import numpy as np
from spatialmath import SE3, Twist3
from spatialmath import base
from math import cos, sin, pi


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()

ss = False
se = False
r = 100
th = 0.3
s=0.8
sp=10
colors = [(0.5,0,0), '#c0c20a', 'blue']


print(pv.__version__)


def add_arrow(p, i, T, opacity=1.0, color=None):

	pos = [0, 0, 0]
	pos[i] = 1.1

	arrow = pv.Arrow(direction=pos, tip_resolution=r, shaft_resolution=r)
	arrow.transform(T)
	if color is None:
		color = colors[i]
	p.add_mesh(arrow, color=color, specular=s, specular_power=sp, smooth_shading=ss, show_edges=se, opacity=opacity)

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
	p.add_mesh(text, color=color, opacity=opacity)

def add_plot(T, opacity=1.0, color=None):

	T = T.A
	add_arrow(plotter, 0, T, opacity=opacity, color=color)
	add_arrow(plotter, 1, T, opacity=opacity, color=color)
	add_arrow(plotter, 2, T, opacity=opacity, color=color)
	plotter.enable_parallel_projection()

def add_line(plotter, p1, p2, radius):
	p1 = base.getvector(p1, 3)
	p2 = base.getvector(p2, 3)
	centre = (p1 + p2) / 2
	dir = p1 - p2
	h = base.norm(p1 - p2)
	plotter.add_mesh(pv.Cylinder(center=centre, direction=dir, radius=radius, height=h))

dir = [-0.2, -0.1, 1]
pos = [0, 2, 0]
# plotter.add_mesh(pv.Cylinder(center=pos, direction=dir, radius=0.1, height=3))

screw = pv.read('LeadScrew.stl')
screw.points /= 40
screw.rotate_x(90)

screw.translate(pos)
plotter.add_mesh(screw)

nut1 = pv.read('nut.stl')
nut1.points /= 2.5

nut2 = nut1.copy()
nut1.translate([0, 2, -2.2])

plotter.add_mesh(nut1)

plotter.add_axes()

S = Twist3.Revolute(q=pos, a=dir, pitch=0.3)

p1 = [0.1, 0.1, -2]
T1 = SE3(p1) * SE3.Rz(-0.9)
T2 = S.exp(3*pi) * T1
p2 = T2.t
add_plot(T1, color='blue')
add_plot(T2, color='red')

add_line(plotter, p1, [0, 2, -2], 0.03)

nut2.translate([0, 2, p2[2]-0.2])
plotter.add_mesh(nut2)
add_line(plotter, p2, [0, 2, p2[2]], 0.03)

plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

# camera position, focus point, up
plotter.camera_position = [(1, 5, 1), (0, 2, -1), (0, 0, 1)]
plotter.show(screenshot='fig2_22.png')