import pyvista as pv

import numpy as np
# from spatialmath import SE3
from spatialmath import base
from math import cos, sin, pi
import pvplus
import roboticstoolbox as rtb

plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000,2000))
print(pv.__version__)

puma = rtb.models.DH.Puma560()

J = puma.jacob0(puma.qn)

Jt = J[:3,:]

E = Jt @ Jt.T
print(E)

e, _ = np.linalg.eig(E)

# the radii are square root of the eigenvalues
radii = np.sqrt(e)
print(radii)

from spatialmath import base
base.plot_ellipsoid(E, inverted=True)

# clf
# puma.vellipse(qns, 'rot')

pvplus.ellipsoid_3d(plotter, E, inverted=True)

# plotter.add_text('boo!', (500, 500))
plotter.set_background('white')

# plotter.show_bounds()

# plotter.add_axes()
# plotter.export_obj('exported.obj')
plotter.show(screenshot='fig8_4a.png')