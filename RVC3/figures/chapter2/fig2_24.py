#! /usr/bin/env python3
import pyvista as pv
import numpy as np
from spatialmath import SE3, Twist3
from spatialmath import base
from math import cos, sin, pi
import rvcprint
from PIL import Image

def add_arrow(i, T):

	pos = [0, 0, 0]
	pos[i] = 1.1

	arrow = pv.Arrow(direction=pos, tip_resolution=r, shaft_resolution=r)
	arrow.transform(T)

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
	return arrow + text

def add_frame(T):

	T = T.A

	mesh = add_arrow(0, T)
	mesh += add_arrow(1, T)
	mesh += add_arrow(2, T)
	return mesh

def add_strut(p1, p2, radius):
	p1 = base.getvector(p1, 3)
	p2 = base.getvector(p2, 3)
	centre = (p1 + p2) / 2
	dir = p1 - p2
	h = base.norm(p1 - p2)
	return pv.Cylinder(center=centre, direction=dir, radius=radius, height=h)

def xform(mesh, T):
	mesh.transform(T.A)

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()

ss = False
se = False
r = 100
th = 0.3
s=0.8
sp=10
colors = [(0.5,0,0), '#c0c20a', 'blue']

# -------------------------------------------------------------------------- #
# create the twist
dir = [-0.2, -0.1, 1]
T0 = SE3.OA([0, 1, 0], dir)
print(T0)
print(np.r_[dir]/np.linalg.norm(dir))
p0 = np.r_[0, 0, 0]
S = Twist3.UnitRevolute(q=p0, a=dir, pitch=0.8)

# -------------------------------------------------------------------------- #
# create the leadscrew, it is in z-direction
screw = pv.read('LeadScrew.stl')
screw.points /= 40
screw.rotate_x(90)
screw.points += np.r_[0, 0, 2]

screw.translate(p0)
xform(screw, T0)

# -------------------------------------------------------------------------- #
# create nut
nut = pv.read('nut.stl')
nut.points /= 2.5
nut.points -= nut.points.mean(axis=0)

# rotate about origin so axis is aligned with leadscrew
xform(nut, T0)

# -------------------------------------------------------------------------- #
# create the assembly: nut + frame + strut

# pose of frame
p1 = [0.8, 0.3, 0]
T1 = SE3(p1) * SE3.Rz(-0.9) * SE3.Rx(0.2)

# merge the meshes
assembly = nut + add_frame(T1) + add_strut(p1, [0, 0, 0], 0.03)

# -------------------------------------------------------------------------- #
# create the scene

# add leadscrew
plotter.add_mesh(screw)

# add initial assembly in blue
plotter.add_mesh(assembly, color='blue')

# add twisted versions of assembly with varying opacity
theta = np.arange(0.25, 4.1, 0.5)
opacity = np.linspace(0.1, 0.7, len(theta))
opacity[-1] = 1

for th, op in zip(theta, opacity):
	assembly_2 = assembly.copy()
	xform(assembly_2, S.SE3(th))
	plotter.add_mesh(assembly_2, color='red', opacity=op)

# -------------------------------------------------------------------------- #
# view and save

# camera position, focus point, up
plotter.camera_position = [(1, 5, 1), (0, 0, 1), (0, 0, 1)]
plotter.set_background('white')

plotter.show(auto_close=False)  # interactive viewing

# grab the frame buffer and save as a file
im = plotter.screenshot()
image = Image.fromarray(im)

out = rvcprint.outfile(format='png')
image.save(out)
