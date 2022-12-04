import numpy as np
from machinevisiontoolbox import *
from matplotlib import cm

# compute disparity
L = Image.Read('rocks2-l.png', reduce=2)
R = Image.Read('rocks2-r.png', reduce=2)
L.mono().disp()
disparity = L.StereoSGBM(R, 3, [40, 90], (4, 100))

# map to world coordinates
b = 0.160 # m
f = 3740  # pixels
di = disparity.image + 274
U, V = L.meshgrid()

u0 = L.width / 2
v0 = L.height / 2

X = b * (U - u0) / di
Y = b * (V - v0) / di
Z = f * b / di

# vars = dict(X=X, Y=Y, Z=Z, image=L.mono().A)
# pickle.dump(vars, open('data.p', 'wb'))

# np.savez('data.npz', X=X, Y=Y, Z=Z, image=L.mono().A, allow_pickle=False)


import numpy as np
from matplotlib import cm

import pyvista as pv

# with np.load('data.npz') as data:
# 	X = data['X']
# 	Y = data['Y']
# 	Z = data['Z']
# 	image = data['image']

image = L.A[...,::-1]

print('Z shape', Z.shape)
print('image shape', image.shape)

grid = pv.StructuredGrid(X, Y, Z)

tex = pv.numpy_to_texture(image[::-1,:])
grid.texture_map_to_plane(inplace=True, use_bounds=True)

plotter = pv.Plotter()
plotter.add_mesh(grid, texture=tex)

plotter.camera_position = np.array(
[(0.07503859607946789, -0.10668551787851316, 0.8259781553143458),
 (-0.00025559105431308127, -0.00025559105431309515, 1.7847194073969184),
 (-0.006901873996314264, -0.9939303744479336, 0.10979423885217895)]
)
plotter.show(window_size=(2000,2000))
print(cpos)
