#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
# from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# compute disparity
L = Image.Read('rocks2-l.png', reduce=1)
R = Image.Read('rocks2-r.png', reduce=1)
disparity = L.stereo_SGBM(R, 3, [2*40, 2*90], (2*200, 2))

# map to world coordinates
b = 0.160 # m
f = 3740  # pixels
di = disparity.image * 2 + 274
U, V = L.meshgrid()

u0 = L.width / 2
v0 = L.height / 2

X = b * (U - u0) / di
Y = b * (V - v0) / di
Z = f * b / di

cam = CentralCamera(f=f, imagesize=L.shape)
pcd = PointCloud(Z, image=L, camera=cam, depth_trunc=1.9)
pcd.transform(SE3.Rx(np.pi))

view = {
			"front" : [ 0.31299127017122574, 0.02154681571003491, 0.9495115583969268 ],
			"lookat" : [ 0.03055555680218866, 0.030925927187669552, -1.1837890148162842 ],
			"up" : [ -0.0343613671057671, 0.99934501124934461, -0.011350988576774189 ],
			"zoom" : 0.69999999999999996
		}


pcd.disp(**view, block=False, file=rvcprint.outfile(format='png'))

## MATPLOTLIB
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.plot_surface(X, Y, Z)
# ax.view_init(-100, -100)
# plt.show(block=True)

# 3D display
# https://github.com/pyvista/pyvista-support/issues/425

## PYVISTA
# interactive = True
# import pyvista as pv
# import vtk
# colors = vtk.vtkNamedColors()

# grid = pv.StructuredGrid(X, Y, Z)
# grid['Z'] = Z.T.ravel()

# plotter = pv.Plotter(off_screen=not interactive)
# plotter.set_background('white')
# # plotter.enable_shadows()

# plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis_r"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)
# plotter.add_scalar_bar(
#     title='',
#     vertical=True,
#     title_font_size=16,
#     label_font_size=60,
#     shadow=False,
#     n_labels=5,
#     italic=False,
#     color='black',
#     fmt="%.2f",
#     font_family="arial",
#     height=0.7,
#     width=0.1,
#     position_x=0.84,
#     position_y=0.1)

# # Y direction light, XZ plane
# light3 = vtk.vtkLight()
# light3.SetFocalPoint(0, 0, 2)
# light3.SetPosition(0, 0, 0)
# light3.SetColor(colors.GetColor3d('white'))
# light3.SetIntensity(0.6)
# plotter.renderer.AddLight(light3)

# # plotter.show_axes()
# cpos = np.array(
#     [(0.054072103377029314, -0.042996756070283346, 1.1274849019097752),
#  (-0.00025559105431308127, -0.00025559105431309515, 1.7847194073969184),
#  (-0.038464076155694915, -0.9973545276682833, 0.06168031278345244)]
# )
# plotter.camera_position = cpos

# if interactive:
#     cpos = plotter.show(window_size=(1024*2, 700*2))
#     print(cpos)

# else:
#     plotter.show(window_size=(1024*4, 768*4), auto_close=False, interactive=False)
#     img = plotter.screenshot(None, return_img=True)
#     plotter.close()

#     print('got image')
#     idisp(img, plain=True, title=None)
#     rvcprint.rvcprint()