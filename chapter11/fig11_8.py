clf
cam = CentralCamera('focal', 0.015, 'pixel', 10e-6, ...
    'resolution', [1280 1024], 'centre', [640 512], 'name', 'mycamera')

cube = mkcube(0.2, 'pose', transl([0, 0, 1]) )
[X,Y,Z] = mkcube(0.2, 'pose', transl([0, 0, 1.0]), 'edge')
cam.mesh(X, Y, Z, 'k')
rvcprint('subfig', 'a', 'hidden', cam.h_image.Parent)

cam.clf
cam.T = transl(-1,0,0.5)*troty(0.8)
cam.mesh(X, Y, Z, 'pose', Tcam, 'k')
rvcprint('subfig', 'b', 'hidden', cam.h_image.Parent)

