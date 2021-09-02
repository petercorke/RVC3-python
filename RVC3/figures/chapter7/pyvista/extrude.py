import pyvista as pv
import numpy as np
from spatialmath import SE3
from math import cos, sin, pi

import pvplus

def zoom(plotter, value):
    if not plotter.camera_set:
        plotter.camera_position = plotter.get_default_cam_pos()
        plotter.reset_camera()
        plotter.camera_set = True
    plotter.camera.Zoom(value)
    plotter.render()
    
# Monkey patch it
pv.Plotter.zoom = zoom

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
overlap = 0.2
r = 100
eer = 0.06
opacity = 0.3
wf = True

q1 = 0.7
q2 = 0.5
q3 = -1
zb = -0.4

T1 = SE3.Rz(q1)

# T2 = SE3.Rz(q1) * SE3.Tx(0.75) * SE3.Ty(0.55) * SE3.Rz(q2)
# T3 = SE3.Rz(q1) * SE3.Tx(1.1) * SE3.Ty(-0.35) * SE3.Rz(q3)

T2 = SE3.Rz(q1) * SE3.Tx(1.2) * SE3.Ty(0.5) * SE3.Rz(q2)
T3 = SE3.Rz(q1) * SE3.Tx(0.6) * SE3.Ty(-0.5) * SE3.Rz(q3)

T2E = T2 * SE3.Tx(1)
T3E = T3 * SE3.Tx(1) 

# ## link 1
# points = np.array([
#     [-0.2,  0.2, 0],
#     [ 0.8,  0.6, 0],
#     [ 1.2,  0.3, 0],
#     [ 1.2, -0.6, 0],
#     [-0.2, -0.2, 0]
#     ])
# N = points.shape[0]
# face = [N + 1] + list(range(N)) + [0]
# polygon = pv.PolyData(points, faces=face)

# L1 = polygon.extrude((0, 0, 0.1))


pvplus.add_frame2(plotter, SE3(0,0,zb), label='0', scale=0.5)


## link 1
L1 = pv.Box(bounds=(-overlap, 1+overlap, -0.6, 0.6, -0.05, 0.05))
L1.transform(T1.A)
plotter.add_mesh(L1, color='red', show_edges=wf, opacity=opacity)

# joint
pvplus.axis(plotter, T1, text='q_0')


# frame
pvplus.add_frame2(plotter, T1, label='1', scale=0.5)


## link 2
L2 = pv.Box(bounds=(-overlap, 1, -0.2, 0.2, -0.05, 0.05))
L2.transform(T2.A)
plotter.add_mesh(L2, color='blue', show_edges=wf, opacity=opacity)

# joint
pvplus.axis(plotter, T2, text='q_1')


## end-effector
EE = pv.Sphere(radius=eer, center=(0,0, 0))
EE.transform(T2E.A)
plotter.add_mesh(EE, color='black')
pvplus.add_frame2(plotter, T2E, scale=0.5, label='E1')


pvplus.add_frame2(plotter, T2, scale=0.5, label='2')


## link 3

pvplus.axis(plotter, T3, text='q_2')


L3 = pv.Box(bounds=(-overlap, 1, -0.2, 0.2, -0.05, 0.05))
L3.transform(T3.A)
plotter.add_mesh(L3, color='blue', show_edges=wf, opacity=opacity)

## end-effector
EE = pv.Sphere(radius=eer, center=(0,0, 0))
EE.transform(T3E.A)
plotter.add_mesh(EE, color='black')

pvplus.add_frame2(plotter, T3, scale=0.5, label='3')
pvplus.add_frame2(plotter, T3E, scale=0.5, label='E2')


# centre the scene in camera view, look along -X axis
plotter.camera_position = [(3.2,-4,1.5), (1, 0, 0), (0, 0, 1)]

plotter.set_background('white')
plotter.disable_parallel_projection()

# plotter.show_axes()  # put a small frame for orientation in bottom left
# plotter.show_bounds(grid='front')  # overlay a grid

zoom(plotter, 1.2)
plotter.save_graphic('fig7_8.svg', raster=False)
plotter.show(screenshot='fig7_8.png')