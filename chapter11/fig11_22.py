[X,Y,Z] = mkcube(1, 'centre', [1, 1, 0.8], 'edge')

cam = SphericalCamera('name', 'spherical')
[X,Y,Z] = mkcube(1, 'centre', [2, 3, 1], 'edge')
cam.mesh(X, Y, Z)

rvcprint('hidden', cam.h_image.Parent)
