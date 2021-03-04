import pyvista as pv
import vtk

import numpy as np
from spatialmath import SE3
from spatialmath import base
from math import cos, sin, pi
import frames


plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
plotter.enable_parallel_projection()
print(pv.__version__)

# from https://github.com/pyvista/pyvista/issues/952


colors = vtk.vtkNamedColors()
colors.SetColor('HighNoonSun', [255, 255, 251, 255])  # Color temp. 5400°K
colors.SetColor('100W Tungsten', [255, 214, 170, 255])  # Color temp. 2850°K

plotter.renderer.RemoveAllLights()

light1 = vtk.vtkLight()
light1.SetFocalPoint(0, 0, 0)
light1.SetPosition(0, 0, 2)
light1.SetColor(colors.GetColor3d('red'))
light1.SetIntensity(0.3)
plotter.renderer.AddLight(light1)

light2 = vtk.vtkLight()
light2.SetFocalPoint(0, 0, 0)
light2.SetPosition(2, 0, 0)
light2.SetColor(colors.GetColor3d('green'))
light2.SetIntensity(0.3)
plotter.renderer.AddLight(light2)

light3 = vtk.vtkLight()
light3.SetFocalPoint(0, 0, 0)
light3.SetPosition(0, 2, 0)
light3.SetColor(colors.GetColor3d('blue'))
light3.SetIntensity(0.3)
plotter.renderer.AddLight(light3)

light4 = vtk.vtkLight()
light4.SetFocalPoint(0, 0, 0)
light4.SetPosition(2, 2, 2)
light4.SetColor(colors.GetColor3d('white'))
light4.SetIntensity(0.3)
plotter.renderer.AddLight(light4)

# Add 3 backing planes
D = 5
z0 = -1.5
T = 0.1
plane_mesh1 = pv.Cube([0, 0, z0], D, D, T)
plane_mesh2 = pv.Cube([-D/2, 0, D/2 + z0], T, D, D)
plane_mesh3 = pv.Cube([0, -D/2, D/2 + z0], D, T, D)

# do the ellipsoid
# ellipsoid = pv.ParametricEllipsoid(xradius=0.9, yradius=1.2, zradius=1)
r = np.r_[113, 48, 1] / 100
R = np.array(
[[-0.99961577, -0.02745518,  0.00381005],
 [-0.00318801,  0.25042309,  0.96813125],
 [ 0.02753434, -0.96774712,  0.2504144 ]])

T = base.r2t(base.trnorm(R).T)
ellipsoid = pv.ParametricEllipsoid(xradius=r[0], yradius=r[1], zradius=r[2])
ellipsoid.transform(T)

# add the meshes to scene
plotter.add_mesh(ellipsoid, ambient=0.5, diffuse=0.5, specular=0.8, specular_power=30,
            smooth_shading=True, color='white')
plotter.add_mesh(plane_mesh1 + plane_mesh2 + plane_mesh3, ambient=0.2)

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
# plotter.enable_eye_dome_lighting()  # messes up subplots
plotter.add_axes()
# plotter.export_obj('exported.obj')
plotter.show(screenshot='fig8_4b.png')