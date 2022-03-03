#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from spatialmath import SE3
import spatialmath.base as smbase

camera = CentralCamera.Default()

#T = transl(0.1, 0.6, -1)*trotz(0.3)*trotx(0.7)
T = SE3(0.1, 0.6, -1) * SE3.Rz(0.3) * SE3.Rx(0.7)

P = mkgrid(2, 0.5)

uv0 = camera.project_point(P, pose=T)
uvf = camera.project_point(P, pose=SE3(0,0,-2))

smbase.plot_polygon(uv0, filled=False, close=True, color='r', linestyle='--')
smbase.plot_polygon(uvf, filled=False, close=True, color='b', linestyle=':')

# smbase.plot_point(uv0, 'o', markerfacecolor='w', markeredgecolor='r', markersize=9, label='initial')
# smbase.plot_point(uvf, '*', markerfacecolor='b', markeredgecolor='b', markersize=9, label='goal')

smbase.plot_polygon(uv0, 'ro--', close=True, color='r', markerfacecolor='w', label='initial view')
smbase.plot_polygon(uvf, 'b*:', close=True, color='b', label='goal view')

for i in range(4):
    #arrow(uv0(:,i), uvf(:,i), 'EdgeColor', 'b')
    smbase.plot_arrow(uv0[:, i], uvf[:, i], width=4, color='k', zorder=20)

plt.xlim(0, camera.width)
plt.ylim(0, camera.height)
plt.legend()
ax = plt.gca()
ax.invert_yaxis()
ax.set_aspect('equal')  
ax.set_facecolor('lightyellow')

plt.grid(True)
plt.xlabel('u (pixels)')
plt.ylabel('v (pixels)')


rvcprint.rvcprint(facecolor=None)
