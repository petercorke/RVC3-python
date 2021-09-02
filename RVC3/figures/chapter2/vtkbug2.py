#! /usr/bin/env python3
import matplotlib.pyplot as plt
import pyvista as pv
import vtk
import pvplus
from spatialmath import SE3
import numpy as np

scale = 2.0
w = 4032
h = 3024

w = int(w / scale)
h = int(h / scale)

plotter = pv.Plotter(polygon_smoothing=True, off_screen=True, window_size=(w, h))
plotter.disable_parallel_projection()
plotter.set_background('white')
plotter.camera_set = True

pvplus.add_frame(plotter, SE3(0, 0, 5), scale=0.1)

fx = 3045.0 / scale
fy = fx

cx = w / 2.0
cy = h / 2.0

K = np.array( [ [ fx, 0., cx],
                [ 0., fx, cy],
                [ 0., 0., 1.]])

cam = plotter.renderer.GetActiveCamera()
near = 0.1
far = 1000.0
cam.SetClippingRange(near, far)



# Set window center for offset principal point
wcx = -2.0 * (cx - w / 2.0) / w
wcy =  2.0 * (cy - h / 2.0) / h
cam.SetWindowCenter(wcx, wcy)

# Set vertical view angle as a indirect way of setting the y focal distance
angle = 180 / np.pi * 2.0 * np.arctan2(h / 2.0, fy)
cam.SetViewAngle(0.1 * angle)
print(angle, cam.GetViewAngle())
plotter.renderer.ResetCameraClippingRange()

# Set the image aspect ratio as an indirect way of setting the x focal distance
m = np.eye(4)
aspect = fy/fx
m[0,0] = 1.0/aspect
t = vtk.vtkTransform()
t.SetMatrix(m.flatten())
cam.SetUserTransform(t)

# Position is at origin, looking in z direction with y down
xoff = 0
cam.SetPosition(xoff, 0, 0)
cam.SetFocalPoint(xoff, 0, 1)
cam.SetViewUp(0, -1, 0)

plotter.camera_set = True

# plotter.show() #screenshot='kitchen.png') #screenshot='fig2_14.png')

plotter.store_image = True  # last_image and last_image_depth
plotter.close()

# get screen image
img = plotter.last_image

# get depth
# img = p.get_image_depth(fill_value=np.nan, reset_camera_clipping_range=False)
# img = p.last_image_depth

plt.figure()
plt.imshow(img)
plt.xlabel('X Pixel')
plt.ylabel('Y Pixel')
plt.show(block=True)