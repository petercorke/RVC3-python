#! /usr/bin/env python3
import pyvista as pv
import vtk
import numpy as np

# change these values
gridlines = True
shadows = True

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.disable_parallel_projection()

sphere = pv.Sphere(radius=0.3, center=(0,0,1))
plotter.add_mesh(sphere, ambient=0.2, diffuse=0.5, specular=0.8, specular_power=30,
            smooth_shading=True, color='dodgerblue')

# add the grid
grid = pv.Plane(i_size=5, j_size=5)
plotter.add_mesh(grid, show_edges=gridlines, ambient=0, diffuse=0.5, specular=0.8, color='red', edge_color='white')

if shadows:
    # do the shadows
    shadows = vtk.vtkShadowMapPass()
    seq = vtk.vtkSequencePass()

    passes = vtk.vtkRenderPassCollection()
    passes.AddItem(shadows.GetShadowMapBakerPass())
    passes.AddItem(shadows)
    seq.SetPasses(passes)

    # Tell the renderer to use our render pass pipeline
    cameraP = vtk.vtkCameraPass()
    cameraP.SetDelegatePass(seq)
    plotter.renderer.SetPass(cameraP)

plotter.set_background('white')
plotter.show()