#!/usr/bin/env python3

import rvcprint
import numpy as np
# from machinevisiontoolbox import *
import pyvista as pv
import matplotlib.pyplot as plt

import pickle
data = pickle.load(open('DSI.p', 'rb'))
DSI = data[2]

# Create the spatial reference
grid = pv.UniformGrid()

# Set the grid dimensions: shape + 1 because we want to inject our values on
#   the CELL data
grid.dimensions = np.array(DSI.shape) + 1

# Edit the spatial reference
# grid.origin = (100, 33, 55.6)  # The bottom left corner of the data set
grid.spacing = (1, 1, 5)  # These are the cell sizes along each axis

# Add the data values to the cell data
grid.cell_arrays["values"] = DSI.flatten(order="F")  # Flatten the array!

# Now plot the grid!
opacity = [0, 0, 0, 0.1, 0.3, 0.6, 1]
grid.plot(show_edges=False, opacity="sigmoid_5")

# slices = grid.slice_orthogonal()
# slices = grid.slice_along_axis(n=6, axis='x')

# cmap = plt.cm.get_cmap("viridis", 4)

# slices.plot(cmap=cmap)

p = pv.Plotter()

# p.add_volume(DSI, cmap="seismic", opacity="sigmoid")


# # slice_along_axis(100, axis='x')
# p.show()



# plotter = pv.Plotter(off_screen=not interactive)
# plotter.set_background('white')
# # plotter.enable_shadows()


# plotter.add_mesh(grid, show_scalar_bar=False, cmap=cm.get_cmap("viridis"), ambient=0.3, diffuse=0.8, specular=0.1, smooth_shading=True)
# plotter.add_scalar_bar(
#     title='',
#     vertical=True,
#     title_font_size=16,
#     label_font_size=60,