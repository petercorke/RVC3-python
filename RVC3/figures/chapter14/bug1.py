import pyvista as pv
from matplotlib import cm
import numpy as np

x = np.arange(-10, 10, 0.25)
y = np.arange(-10, 10, 0.25)
x, y = np.meshgrid(x, y)
r = np.sqrt(x ** 2 + y ** 2)
z = np.sin(r)

grid = pv.StructuredGrid(x, y, z)
print('z range is', z.min(), z.max())

plotter = pv.Plotter()
plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)

plotter.add_scalar_bar(title='Distance (m)',
    vertical=True,
    title_font_size=16,
    label_font_size=16,
    height=0.6,
    width=0.1,
    position_x=0.8,
    position_y=0.2)

plotter.show()