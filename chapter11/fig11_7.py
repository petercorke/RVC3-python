import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter


cam = CentralCamera('focal', 0.015)
P = [0.3, 0.4, 3.0]'
cam.project(P)
cam.project(P, [], transl(-0.5, 0, 0) )
cam = CentralCamera('focal', 0.015, 'pixel', 10e-6, ...
    'resolution', [1280 1024], 'centre', [640 512], 'name', 'mycamera')
cam.project(P)
cam.C
cam.K
cam.fov[] * 180/pi
P = mkgrid(3, 0.2, 'T', transl(0, 0, 1.0))

cam.project(P)
cam.plot(P)
rvcprint('subfig', 'a', 'hidden', cam.h_image.Parent)

Tcam = transl(-1,0,0.5)*troty(0.9)
cam.plot(P, 'pose', Tcam)
rvcprint('subfig', 'b', 'hidden', cam.h_image.Parent)

