## camera calibration and decomposition

# create "unknown" camera
P = mkcube(0.2)
T_unknown = transl(0.1, 0.2, 1.5) * rpy2tr(0.1, 0.2, 0.3)
cam_unknown = CentralCamera('name', 'true', 'focal', 0.015, ...
    'pixel', 10e-6, 'resolution', [1280 1024], 'centre', [512 512], ...
    'noise', 0.05)
p = cam_unknown.project(P, 'objpose', T_unknown)

# calibrate it
C = camcald(P, p)

# decompose it to parameters
est = invcamcal(C)
est.f/est.rho[0]
cam_unknown.f/cam_unknown.rho[1]
T_unknown*est.T

clf
hold on
plot_sphere(P, 0.03, 'r')
tformplot(eye[3,3], 'frame', 'T', 'color', 'b', 'length', 0.3)
est.plot_camera('color', 'b')
#cam_unknown.plot_camera('Tcam', inv(T_unknown), 'color', 'r')
xyzlabel
view[53,15]
lighting gouraud
light
axis equal
grid

rvcprint('opengl')
