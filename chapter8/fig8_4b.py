import pyvista as pv
import numpy as np
from spatialmath import SE3

plotter = pv.Plotter(shape=(2,3), border=False, polygon_smoothing=True, window_size=(2000,1000))
plotter.enable_parallel_projection()


plotter.add_axes()


ellipsoid = pv.ParametricEllipsoid(xradius=0.2, yradius=1, zradius=1.2)
plotter.add_mesh(ellipsoid, ambient=0.5, diffuse=0.5, specular=0.8, specular_power=30,
            smooth_shading=True, color='orange')

ellipsoid.save('ellipsoid.ply')
plotter.set_background('white')
# plotter.enable_eye_dome_lighting()  # messes up subplots

plotter.export_obj('ellipse')
plotter.export_vtkjs('ellipse')

plotter.show() #screenshot='screw.png')

