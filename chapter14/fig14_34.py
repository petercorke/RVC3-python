#!/usr/bin/env python3

import rvcprint
import numpy as np
# import matplotlib.pyplot as plt
from machinevisiontoolbox import *
# from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# compute disparity
L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)
disparity = L.StereoSGBM(R, 3, [40, 90], (4, 100))

# map to world coordinates
b = 0.160 # m
f = 3740  # pixels
di = disparity.image + 274
U, V = L.meshgrid()

u0 = L.width / 2
v0 = L.height / 2

X = b * (U - u0) / di
Y = b * (V - v0) / di
Z = f * b / di

# 3D display
# https://github.com/pyvista/pyvista-support/issues/425

interactive = True


import pyvista as pv
import vtk
colors = vtk.vtkNamedColors()

grid = pv.StructuredGrid(X, Y, Z)
grid['Z'] = Z.T.ravel()

plotter = pv.Plotter(off_screen=not interactive)
plotter.set_background('white')
# plotter.enable_shadows()


plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)
plotter.add_scalar_bar(
    title='',
    vertical=True,
    title_font_size=16,
    label_font_size=60,
    shadow=False,
    n_labels=5,
    italic=False,
    color='black',
    fmt="%.2f",
    font_family="arial",
    height=0.7,
    width=0.1,
    position_x=0.84,
    position_y=0.1)

# Y direction light, XZ plane
light3 = vtk.vtkLight()
light3.SetFocalPoint(0, 0, 2)
light3.SetPosition(0, 0, 0)
light3.SetColor(colors.GetColor3d('white'))
light3.SetIntensity(0.6)
plotter.renderer.AddLight(light3)

# plotter.show_axes()
cpos = np.array(
    [(0.054072103377029314, -0.042996756070283346, 1.1274849019097752),
 (-0.00025559105431308127, -0.00025559105431309515, 1.7847194073969184),
 (-0.038464076155694915, -0.9973545276682833, 0.06168031278345244)]
)
plotter.camera_position = cpos

if interactive:
    cpos = plotter.show(window_size=(1024*2, 700*2))
    print(cpos)

else:
    plotter.show(window_size=(1024*4, 768*4), auto_close=False, interactive=False)
    img = plotter.screenshot(None, return_img=True)
    plotter.close()

    print('got image')
    idisp(img, plain=True, title=None)
    rvcprint.rvcprint()