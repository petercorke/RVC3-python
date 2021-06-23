# #!/usr/bin/env python3

# import rvcprint
# import numpy as np
# import matplotlib.pyplot as plt
# from machinevisiontoolbox import *
# from matplotlib.ticker import ScalarFormatter
# from matplotlib import cm

# X = b*(U-u0) ./ di  Y = b*(V-v0) ./ di; Z = 3740 * b ./ di
# Lcolor = iread('rocks2-l.png')
# clf
# surface(X, Y, Z, Lcolor, 'FaceColor', 'texturemap', ...
#    'EdgeColor', 'none', 'CDataMapping', 'direct')
# xyzlabel
# set(gca,'ZDir', 'reverse') set(gca,'XDir', 'reverse')
# view(-84, 44)

# rvcprint.rvcprint('svg')

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

interactive = False


import pyvista as pv
import vtk
colors = vtk.vtkNamedColors()

grid = pv.StructuredGrid(X, Y, Z)

plotter = pv.Plotter(off_screen=interactive)
plotter.set_background('white')
# plotter.enable_shadows()

# image = L.asint()[::-1,:,:].reshape(L.shape, order='C')
image = L.mono().asint()[::-1,:]
L.mono().disp()
tex = pv.numpy_to_texture(image)
# tex = pv.numpy_to_texture(L.A)
grid.texture_map_to_plane(inplace=True)
grid.plot(texture=tex)
# plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)


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