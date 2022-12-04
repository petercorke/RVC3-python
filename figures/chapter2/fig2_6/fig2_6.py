#! /usr/bin/env python3
from machinevisiontoolbox import *
import cv2
import matplotlib.pyplot as plt
import pyvista as pv
import vtk
import pvplus

scene = Image('IMG_8787.JPG')

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)

markers, ids, _ = cv2.aruco.detectMarkers(scene.image, dictionary)

print(ids)
print(markers)


# for id, corners in zip(ids, markers):
#     plot_point(corners.T, 'bs')
#     centre = np.mean(corners, axis=1)
    # plot_point(tuple(centre.flatten()), 'yo', text=f"{id[0]}", color='yellow')


# plt.show(block=True)
# cv2.aruco.drawDetectedMarkers(scene.image, markers)


f = 3045.0  # focal length of the camera in units of pixels (wild guess)
side = 0.067  # the side length of the marker in units of metres

K = np.array([[f, 0, 2016], [0, f, 1512], [0, 0, 1]])
print(K)

rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(markers, side, K, None)
print(tvecs)
print(rvecs)


for i, (t, r) in enumerate(zip(tvecs, rvecs)):
    cv2.drawFrameAxes(scene.image, K, np.zeros((4,)), r, t, 0.1, 20)
scene.disp()

plt.figure()
T = SE3.Alloc(len(ids))
for i, (t, r) in enumerate(zip(tvecs, rvecs)):
    T[i] = SE3(t.flatten()) * SE3.EulerVec(r.flatten())
    # T[i] = T[i].inv()
    T[i].plot(frame=str(i), length=0.1)

print(T)

# plt.show(block=True)

scale = 2.0
w = 4032
h = 3024

w = int(w/scale)
h = int(h/scale)

print(scene.shape)
plotter = pv.Plotter(border=False, polygon_smoothing=True, window_size=(w, h))
plotter.disable_parallel_projection()
plotter.set_background('black')
plotter.camera_set = True

for Tk in T:
    pvplus.add_frame(plotter, Tk, scale=0.1)

# pvplus.add_frame(plotter, SE3(5, 0, 0), scale=0.1)

# plotter.show() #screenshot='fig2_14.png')

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

# Position is at origin, looking in z direction with y down
cam.SetPosition(0, 0, 0)
cam.SetFocalPoint(0, 0, 1)
cam.SetViewUp(0, -1, 0)

# Set window center for offset principal point
wcx = -2.0*(cx - w / 2.0) / w
wcy =  2.0*(cy - h / 2.0) / h
cam.SetWindowCenter(wcx, wcy)

# Set vertical view angle as a indirect way of setting the y focal distance
angle = 180 / np.pi * 2.0 * np.arctan2(h / 2.0, fy)
cam.SetViewAngle(10 * angle)

# Set the image aspect ratio as an indirect way of setting the x focal distance
# m = np.eye(4)
# aspect = fy/fx
# m[0,0] = 1.0/aspect
# t = vtk.vtkTransform()
# t.SetMatrix(m.flatten())
# cam.SetUserTransform(t)

plotter.camera_set = True

x, y = plotter.show(screenshot='kitchen.png') #screenshot='fig2_14.png')
print(scene.shape, y.shape)

mix = Image(y + scene.rgb)

mix.disp()
plt.show(block=True)


