#! /usr/bin/env python3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np



class CameraVisualizer:
    """
    Class for visualizer of a camera object. Used to generate frustrums in
    Matplotlib

        Constructor:
        `CamVisualizer(parameters)
            camera Camera object being visualized
            f_length  length of the frustrum
            fb_width  width of base of frustrum (camera centre end)
            ft_width  width of top of frustrum (lens end)
        Methods:
          gen_frustrum_poly()  return 4x4x3 matrix of points to create
          Poly3DCollection with Matplotlib
                           Order of sides created [top, right, bottom, left]
    """

    def __init__(self, camera, length=0.1, widthb=0.05, widtht=0.1):
        """
        Create instance of CamVisualizer class

        Required parameters: camera  Camera object being visualized (see
            common.py for Camera class)

        Optional parameters: f_length length of the displayed frustrum (0.1
            default) fb_width width of the base of displayed frustrum (camera
            centre end) (0.05 default) ft_width width of the top of displayed
            frustrum (lens end) (0.1 default)
        """
        self.camera = camera

        # Define corners of polygon in cameras frame (cf) in homogenous
        # coordinates b is base t is top rectangle

        widthb /= 2
        widtht /= 2
        self.b0 = np.array([-widthb, -widthb, 0, 1])
        self.b1 = np.array([-widthb, widthb, 0, 1])
        self.b2 = np.array([widthb, widthb, 0, 1])
        self.b3 = np.array([widthb, -widthb, 0, 1])
        self.t0 = np.array([-widtht, -widtht, length, 1])
        self.t1 = np.array([-widtht, widtht, length, 1])
        self.t2 = np.array([widtht, widtht, length, 1])
        self.t3 = np.array([widtht, -widtht, length, 1])

    def gen_frustrum_poly(self):

        # Transform frustrum points to world coordinate frame using the camera
        # extrinsics
        # T = self.camera.pose.A
        T = np.eye(4)

        # bottom/narrow end
        b0 = (T @ self.b0)[:-1]
        b1 = (T @ self.b1)[:-1]
        b2 = (T @ self.b2)[:-1]
        b3 = (T @ self.b3)[:-1]

        # wide/top end
        t0 = (T @ self.t0)[:-1]
        t1 = (T @ self.t1)[:-1]
        t2 = (T @ self.t2)[:-1]
        t3 = (T @ self.t3)[:-1]

        # Each set of four points is a single side of the Frustrum
        # points = np.array([[b0, b1, t1, t0], [b1, b2, t2, t1], [
        #                   b2, b3, t3, t2], [b3, b0, t0, t3]])
        points = [
            np.array([b0, b1, t1, t0]),
            np.array([b1, b2, t2, t1]), 
            np.array([b2, b3, t3, t2]),
            np.array([b3, b0, t0, t3])
        ]
        return points

fig = plt.figure()
ax = plt.axes(projection='3d')

# p0 = [0, 0, 0]
# p1 = [0, 0, 1]
# p2 = [0, 1, 1]
# p3 = [0, 1, 0]
# p4 = [1, 0, 1]
# p5 = [1, 0, 0]

# f1 = np.array([p0, p1, p4, p5])
# f2 = np.array([p0, p1, p2, p3])
# print(f1)
# print(f2)
# polys = Poly3DCollection([f1, f2], facecolors=['g', 'r'])
# 


camfrustum = CameraVisualizer(None,
                                length=0.5,
                                widthb=0.05,
                                widtht=0.5)

polys = Poly3DCollection(camfrustum.gen_frustrum_poly(),
                                              facecolors=['g', 'r', 'b', 'y'])
ax.add_collection3d(polys)
# facecolors=['g', 'r', 'b', 'y'])

