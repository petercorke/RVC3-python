# cube via fisheye camera

cam = CentralCamera('focal', 0.015, 'pixel', 10e-6, ...
    'resolution', [1280 1024], 'centre', [640 512])
P = mkcube(0.2)
T_unknown = transl[-1,-1,1]*trotx(0.1)*troty(0.2)
p = cam.project(P, 'objpose', T_unknown)
T_est = cam.estpose(P, p)
randinit
cam = FishEyeCamera('name', 'fisheye', ...
         'projection', 'equiangular', ...
         'pixel', 10e-6, ...
         'resolution', [1280 1024])
[X,Y,Z] = mkcube(0.2, 'centre', [0.2, 0, 0.3], 'edge')
cam.mesh(X, Y, Z)

rvcprint('hidden', cam.h_image.Parent)
