# pvplus - PyVista extras for drawing coordinate frames, axes and ellipsoids

import pyvista as pv
import numpy as np
from spatialmath import base
from math import cos, sin, pi
import vtk
from spatialmath import SE3
import os.path
import sys
from pathlib import Path
from PIL import Image
"""

HINTS

not very good at display coordinate frames/axes

plotter.show_axes()  put a small frame for orientation in bottom left
plotter.show_bounds(grid='front')  overlay a grid

pv.save("mesh.vtk")
pv.save_meshio("mesh.obj", mesh)

plotter.export_obj(filename)
plotter.export_vtkjs(filename)

"""
s=0.8
sp=10
ss = False
se = False
th = 0.3
r = 100
zl = -0.4


def string(text, subscript=None, scale=1):

    if '_' in text:
        z = text.split('_')
        text = z[0]
        subscript = z[1]

    # create the axis name
    textmesh = pv.Text3D(text, depth=th)

    # add the subscript
    if subscript is not None:
        submesh = pv.Text3D(subscript, depth=th)
        submesh.points /= 1.5  # smaller

        # shift it to the right and down a bit
        m = np.max(textmesh.points, axis=0)


        submesh.translate([m[0] * 0.9, -m[1] * 0.5, 0])
        textmesh = textmesh + submesh  # append it

    # centre the whole thing
    textmesh.points -= np.mean(textmesh.points, axis=0)

    # scale the text
    textmesh.points *= scale / 5
    return textmesh

def add_arrow(p, T, i, color='silver', label=None, subscript=None, scale=1.0, opacity=1.0):

    pos = [0, 0, 0]
    pos[i] = 1.1 * scale

    ## create the arrow to scale
    arrow = pv.Arrow(direction=pos, tip_resolution=r, shaft_resolution=r)
    arrow.points *= scale

    arrow.transform(T, inplace=True)
    p.add_mesh(arrow, color=color, specular=s, specular_power=sp, \
        smooth_shading=ss, show_edges=se, opacity=opacity)

    names = 'XYZ'

    ## create the axis label text to scale

    # create the axis name
    text = pv.Text3D(names[i], depth=th)

    # add the subscript
    if label is not None:
        axlabel = pv.Text3D(label, depth=th)
        axlabel.points /= 1.5  # smaller

        # shift it to the right and down a bit
        m = np.max(text.points, axis=0)
        axlabel.translate([m[0] * 0.8, -m[1] * 0.5, 0])
        text = text + axlabel  # append it

    # centre the whole thing
    text.points -= np.mean(text.points, axis=0)

    # scale the text
    text.points *= scale / 5

    # now orient it in space, rotate about centre
    if i == 0:
        text.rotate_x(90)
    elif i == 1:
        text.rotate_y(90)
        text.rotate_x(90)
    elif i == 2:
        text.rotate_x(90)
        text.rotate_z(90)

    text.translate(pos)
    text.transform(T, inplace=True)

    ## combine arrow and text
    p.add_mesh(text, color=color, opacity=opacity)
    return arrow + text

def add_frame(plotter, T=None, color=None, **kwargs):

    if color is None:
        colors = ['red', 'green', 'blue']
    else:
        colors = (color,) * 3

    if T is None:
        T = SE3()

    T = T.A
    add_arrow(plotter, T, 0, color=colors[0], **kwargs)
    add_arrow(plotter, T, 1, color=colors[1], **kwargs)
    add_arrow(plotter, T, 2, color=colors[2], **kwargs)

def add_frame2(plotter, T, color=None, **kwargs):

    if color is None:
        colors = ['red', 'green']
    else:
        colors = (color,) * 2

    T = T.A
    add_arrow(plotter, T, 0, color=colors[0], **kwargs)
    add_arrow(plotter, T, 1, color=colors[1], **kwargs)



def ribbon(
        length=0.75,
        head=0.15,
        r=0.2,
        w=[0.2, 0.3],
        N=100,
        reverse=False,
        phase=0,
        T=None,
    ):

    length *= 2 * pi
    head *= 2 * pi
    phase *= 2 * pi
    delta = length / N
    Nh = int(head / delta)
    Nt = int(length / delta) - Nh

    if reverse:
        delta = -delta

    w1 = w[0] / 2
    w2 = w[1] / 2

    vertices = np.array([r * cos(phase), r * sin(phase), 0])
    faces = np.array([
        [3, 0, 1, 2],
        [3, 0, 2, 3]
        ])
    # arrow
    #   3 * Nh + 1 vertices
    #   4 (Nh - 1) + 2 faces
    for i in range(1, Nh):
        w = w2 * (i + 1) / Nh
        theta = phase  +(i + 1) * delta

        x = r * cos(theta)
        y = r * sin (theta)
        vertices = np.vstack([
            vertices,
            [x, y, w],
            [x, y, 0],
            [x, y, -w]])

        k = 3 * (i - 1)

        if i < (Nh - 1):
            faces = np.vstack([
                faces,
                [3, 1 + k, 4 + k, 5 + k],
                [3, 1 + k, 5 + k, 2 + k],
                [3, 3 + k, 2 + k, 5 + k],
                [3, 3 + k, 5 + k, 6 + k]])

        theta_h = theta
        nv_h = vertices.shape[0]

    # tail

    for i in range(0, Nt):
        theta = theta_h + i * delta

        x = r * cos(theta)
        y = r * sin (theta)
        vertices = np.vstack([
            vertices,
            [x, y, w1],
            [x, y, 0],
            [x, y, -w1]])

        k = nv_h + 3 * i - 1

        if i < (Nt - 1):
            faces = np.vstack([
                faces,
                [3, 1 + k, 4 + k, 2 + k],
                [3, 2 + k, 4 + k, 5 + k],
                [3, 2 + k, 5 + k, 6 + k],
                [3, 2 + k, 6 + k, 3 + k]])


    shape = pv.PolyData(vertices, faces)
    if T is not None:
        shape.transform(T.A, inplace=True)
    return shape

def axis(plotter, T=None, text=None, direction=(0,0,1), square=False, twist=0.5):

    if square:
        arrow = pv.Arrow(direction=direction, tip_resolution=4, \
            shaft_resolution=4, shaft_radius=0.03,
            tip_radius=0.08, tip_length=0.2)
    else:
        arrow = pv.Arrow(direction=(0,0,1), tip_resolution=r, \
            shaft_resolution=r, shaft_radius=0.03,
            tip_radius=0.08, tip_length=0.2)

    if T is None:
        T = SE3()
    T = SE3(T.t)  # remove rotation
    Ta = T * SE3(0, 0, zl)
    Tr = T * SE3(0, 0, 0.2)
    arrow.transform(Ta.A, inplace=True)
    rib = ribbon(reverse=True, r=0.1, w=[0.12, 0.2], phase=0.08)
    rib.transform(Tr.A, inplace=True)
    plotter.add_mesh(arrow)
    plotter.add_mesh(rib, color='#808080')

    if text is not None:
        t = string(text, scale=0.5)
        t.transform((T  * SE3(0, 0, zl) * SE3(np.r_[direction] * 1.1) * SE3.Rz(twist) * SE3.Rx(pi/2) ).A, inplace=True)
        plotter.add_mesh(t)

def add_ellipsoid(plotter, A, inverted=False, **kwargs):

    if not inverted:
        A = np.linalg.inv(A)

    # compute eigenvalues and vectors
    e, x = np.linalg.eig(A)

    # the radii are square root of the eigenvalues
    radii = np.sqrt(e)
    ellipsoid = pv.ParametricEllipsoid(xradius=radii[0], yradius=radii[1], zradius=radii[2])

    # now orient it
    R = np.real(x)
    T = base.r2t(R)
    ellipsoid.transform(T, inplace=True)

    plotter.add_mesh(ellipsoid, **kwargs)

    return ellipsoid

def ellipsoid_3d(plotter, A, **kwargs):

    plotter.disable_parallel_projection()

    colors = vtk.vtkNamedColors()

    plotter.renderer.RemoveAllLights()

    # top light, XY plane
    light1 = vtk.vtkLight()
    light1.SetFocalPoint(0, 0, 0)
    light1.SetPosition(0, 0, 2)
    light1.SetColor(colors.GetColor3d('white'))
    light1.SetIntensity(1)
    plotter.renderer.AddLight(light1)

    # X direction light, YZ plane
    light2 = vtk.vtkLight()
    light2.SetFocalPoint(0, 0, 0)
    light2.SetPosition(2, 0, 0)
    light2.SetColor(colors.GetColor3d('white'))
    light2.SetIntensity(1)
    plotter.renderer.AddLight(light2)

    # Y direction light, XZ plane
    light3 = vtk.vtkLight()
    light3.SetFocalPoint(0, 0, 0)
    light3.SetPosition(0, 2, 0)
    light3.SetColor(colors.GetColor3d('white'))
    light3.SetIntensity(1)
    plotter.renderer.AddLight(light3)

    # Add 3 backing planes
    D = 5
    z0 = -D / 2
    T = 0.02
    plane_mesh1 = pv.Cube([0, 0, z0], D, D, T)
    plane_mesh2 = pv.Cube([-D/2, 0, D/2 + z0], T, D, D)
    plane_mesh3 = pv.Cube([0, -D/2, D/2 + z0], D, T, D)
    # add the meshes to scene
    plotter.add_mesh(plane_mesh1 + plane_mesh2 + plane_mesh3,
        show_edges=True, ambient=0.3, diffuse=0.8, specular=0.8, specular_power=30, smooth_shading=True)

    # do the ellipsoid
    e = add_ellipsoid(plotter, A, ambient=0.5, diffuse=0.5, specular=0.8, specular_power=30,
                smooth_shading=True, color='dodgerblue', **kwargs)

    # do the shadows
    plotter.renderer.SetUseShadows(True)

if __name__ == "__main__":

    from spatialmath import SE3

    plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))

    # add_frame(plotter, SE3())

    # data from RVC2 fig 8.4b
    # A = np.array([
    # 		[ 0.0076,    0.0000,   -0.0868],
    # 		[ 0.0000,    3.0000,   -0.0000],
    # 		[-0.0868,   -0.0000,    2.9924]
    # 	])
    # e = add_ellipsoid(plotter, A, inverted=True, color='skyblue', style='wireframe')
    # e.plot(show_grid=True)

    add_frame(plotter, SE3())

    plotter.set_background('white')
    plotter.enable_parallel_projection()
    # plotter.show_axes()
    # plotter.show_bounds(grid='front')
    plotter.show()

def outfile(format='png'):
    # build the path for saving, next to the calling script (whatever
    # figures/... directory it happens to live in), not a hardcoded
    # personal path
    script_dir = Path(sys.argv[0]).resolve().parent
    figure = os.path.basename(sys.argv[0])
    figure = os.path.splitext(figure)[0] + '.' + format
    return str(script_dir / figure)



def zoomplot(plotter, value):
    if not plotter.camera_set:
        plotter.camera_position = plotter.get_default_cam_pos()
        plotter.reset_camera()
        plotter.camera_set = True
    plotter.camera.Zoom(value)
    plotter.render()

margin = 5

def cropimage(im):

    bg = []

    def limits(a):
        s = a.index(False) - margin
        if s < 0:
            s = 0

        a.reverse()
        e = a.index(False) - margin
        if e < 0:
            e = 0
        e = len(a) - e

        return s, e

    for c in range(im.shape[1]):
        column = im[:,c,:3]
        t = np.all(column == (255, 255, 255))
        bg.append(t)

    c1, c2 = limits(bg)

    bg = []
    for r in range(im.shape[0]):
        row = im[r,:,:3]
        t = np.all(row == (255, 255, 255))
        bg.append(t)

    r1, r2 = limits(bg)

    print(f"image: rows {r1}-{r2}, columns {c1}-{c2}")

    return im[r1:r2, c1:c2, :]


def save(plotter, show=True, zoom=None, crop=True):
    # output file name
    out = outfile()

    # configure PyVista
    plotter.set_background('white')

    plotter.off_screen = not show

    if zoom is not None:
        zoomplot(plotter, zoom)

    if show:
        # plotter.save_graphic('ZZZ.png', raster=False)
        plotter.show()
    else:
        im = plotter.screenshot()
        print(im.shape)
        if crop:
            im = cropimage(im)

        image = Image.fromarray(im)
        image.save(out)

        # plotter.save_graphic('fig7_2b.png', raster=False)

        print('saving plotter --> ', out)
