#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3, Twist3
from spatialmath import base
from math import cos, sin, pi
import rvcprint

class myPlotter(pv.Plotter):
	def add_arrow(self, i, T, opacity=1.0, color=None):

		pos = [0, 0, 0]
		pos[i] = 1.1

		arrow = pv.Arrow(direction=pos, tip_resolution=r, shaft_resolution=r)
		arrow.transform(T)
		if color is None:
			color = colors[i]
		self.add_mesh(arrow, color=color, specular=s, specular_power=sp, smooth_shading=ss, show_edges=se, opacity=opacity)

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
		self.add_mesh(text, color=color, opacity=opacity)

	def add_frame(self, T, opacity=1.0, color=None):

		T = T.A
		self.add_arrow(0, T, opacity=opacity, color=color)
		self.add_arrow(1, T, opacity=opacity, color=color)
		self.add_arrow(2, T, opacity=opacity, color=color)
		self.enable_parallel_projection()

	def add_strut(self, p1, p2, radius):
		p1 = base.getvector(p1, 3)
		p2 = base.getvector(p2, 3)
		centre = (p1 + p2) / 2
		dir = p1 - p2
		h = base.norm(p1 - p2)
		self.add_mesh(pv.Cylinder(center=centre, direction=dir, radius=radius, height=h))

# class myMesh(pv.PolyData):
# 	@classmethod
# 	def read(cls, filename):
# 		return cls(pv.read(filename))

# 	def xform(self, T):
# 		self.transform(T.A)

# 	def foo(self):
# 		print('foo')

def xform(mesh, T):
	mesh.transform(T.A)

plotter = myPlotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()

ss = False
se = False
r = 100
th = 0.3
s=0.8
sp=10
colors = [(0.5,0,0), '#c0c20a', 'blue']

print(pv.__version__)

# create the twist
dir = [-0.2, -0.1, 1]
T0 = SE3.OA([0, 1, 0], dir)
print(T0)
print(np.r_[dir]/np.linalg.norm(dir))
p0 = np.r_[0, 0, 0]
S = Twist3.UnitRevolute(q=p0, a=dir, pitch=0.3)

# draw the leadscrew, it is in z-direction, symmetric either side of z=0
screw = pv.read('LeadScrew.stl')
screw.points /= 40
screw.rotate_x(90)

screw.translate(p0)
xform(screw, T0)
plotter.add_mesh(screw)

# draw nut 1, 0.2 units tall
nut1 = pv.read('nut.stl')
nut1.points /= 2.5
nut1.points -= nut1.points.mean(axis=0)
nut2 = nut1.copy()

xform(nut1, T0)
plotter.add_mesh(nut1, color='blue')

# x = nut1.copy()
# xform(x, S.SE3(0))
# plotter.add_mesh(x, color='blue')
y = nut2.copy()
xform(y, S.SE3(1))
plotter.add_mesh(y, color='red')

S.SE3(1).printline()

# ##
# T = S.SE3(1) * SE3(0, 0, 0.5)
# nut2.transform(T.A)
# plotter.add_mesh(nut2)
# ##



# add first (blue) coordinate frame
p1 = [0.8, 0.3, 0]
T1 = SE3(p1) * SE3.Rz(-0.9) * SE3.Rx(0.2)
plotter.add_frame(T1, color='blue')

plotter.add_strut(p1, [0, 0, 0], 0.03)

# # add second (red) coordinate frame
# T2 = S.SE3(3*pi) * T1
# add_frame(T2, color='red')

# p2 = T2.t
# nut2.translate([0, 2, p2[2]-0.2])
# plotter.add_mesh(nut2)
# add_strut(plotter, p2, [0, 2, p2[2]], 0.03)

# plotter.set_background('white')
# # plotter.enable_eye_dome_lighting()  # messes up subplots

# draw the reference coordinate frame
plotter.add_axes()

# camera position, focus point, up
plotter.camera_position = [(1, 5, 1), (0, 2, -1), (0, 0, 1)]
plotter.show(screenshot=rvcprint.outfile(format='png'))
