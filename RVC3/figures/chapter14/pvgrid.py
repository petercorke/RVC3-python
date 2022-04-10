import pyvista as pv
import numpy as np

x = np.arange(-10, 10, 0.25)
y = np.arange(-10, 10, 0.25)
z = np.arange(-10, 10, 0.25)
x, y, z = np.meshgrid(x, y, z)

# create the unstructured grid directly from the numpy arrays and plot
grid = pv.StructuredGrid(x, y, z)
# grid['Z'] = Z.T.ravel()

# grid.plot(show_edges=True)

# # plotter.set_background('white')
# # # plotter.enable_shadows()


# # plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)
# # plotter.add_scalar_bar(
# #     title='',
# #     vertical=True,
# #     title_font_size=16,
# #     label_font_size=60,


# import pyvista as pv
# from pyvista import examples

# # Download a volumetric dataset
# vol = examples.download_knee_full()

# # A nice camera position
# cpos = [(-381.74, -46.02, 216.54), (74.8305, 89.2905, 100.0), (0.23, 0.072, 0.97)]

# vol.plot(volume=True, cmap="bone", cpos=cpos)