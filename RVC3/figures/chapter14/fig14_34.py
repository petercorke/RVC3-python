#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt

# from machinevisiontoolbox import *
# from mayavi import mlab
# from mayavi.api import Engine
from machinevisiontoolbox import *

L = Image.Read('rocks2-l.png', dtype='float32', reduce=2)
R = Image.Read('rocks2-r.png', dtype='float32', reduce=2)

disparity, similarity, DSI = L.stereo_simple(R, 3, [40, 90])

print(DSI.shape)

fig, axes = plt.subplots(ncols=2, nrows=2, sharey=True, sharex=True)
# d = plt.subplot_mosaic('ABb;CDb')
for i, (ax, v) in enumerate(zip(axes.ravel(), np.arange(100, 541, 100))):
    mappable = ax.imshow(DSI[v, :, :].T)
    ax.set_xlim(0, DSI.shape[0])
    ax.set_ylim(0, 50)
    ax.set_aspect('auto')
    ax.text(420, 3, f"v={v}", backgroundcolor="white")
    if i > 1:
        ax.set_xlabel('u (pixels)')
    if i % 2 == 0:
        ax.set_ylabel('disparity (pixels)')

plt.subplots_adjust(bottom=0.1, right=0.85, top=0.9)
cax = plt.axes([0.88, 0.1, 0.03, 0.8])
plt.colorbar(mappable, cax=cax)
# fig.colorbar(mappable)


# try:
#     engine = Engine()
# except NameError:
#     from mayavi.api import Engine
#     engine = Engine()
#     engine.start()

# if len(engine.scenes) == 0:
#     engine.new_scene()


# axes = mlab.axes() #extent=(0, DSI.shape[0], 0, DSI.shape[1], 0, DSI.shape[2]))
# axes.label_text_property.bold = False
# axes.label_text_property.italic = False
# axes.label_text_property.font_size = 2
# axes.title_text_property.font_size = 2

# for v in np.arange(60, 541, 100):
#     mlab.volume_slice(DSI, plane_orientation='x_axes', slice_index=v, colormap='seismic')
# mlab.xlabel('v (pixels)')
# mlab.ylabel('u (pixels)')
# mlab.zlabel('disparity (pixels)')
# bar = mlab.scalarbar(title='ZNCC similarity', orientation='vertical')
# mlab.outline()

# ltp = bar._get_label_text_property()
# ltp.font_size=2
# # module_manager4 = engine.scenes[0].children[4].children[0]
# bar.scalar_bar_representation.maximum_size = np.array([1000, 1000])
# bar.scalar_bar_representation.minimum_size = np.array([1, 1])
# bar.scalar_bar_representation.position = np.array([0.9, 0.1])  # top left
# bar.scalar_bar_representation.position2 = np.array([0.1, 0.8]) # width height

# scene = engine.scenes[0]
# scene.scene.camera.position = [1173.485170290038, 894.8394829909678, 583.3499021831709]
# scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
# scene.scene.camera.view_angle = 30.0
# scene.scene.camera.view_up = [-0.3936322021725195, -0.2379005029285883, 0.8879510347531203]
# scene.scene.camera.clipping_range = [441.614360447841, 2152.948893224912]
# scene.scene.camera.compute_view_plane_normal()
# scene.scene.render()

# mlab.show()

# view(-52,18)
# shading interp

# h = colorbar
# h.Label.String = 'ZNCC similarity'
# h.Label.FontSize = 10

# xlabel('u (pixels)') ylabel('v (pixels)'); zlabel('d (pixels)')

# # DSI(1,:,:) = 0
# # DSI(end,:,:) = 0
# # DSI(:,1,:) = 0
# # DSI(:,end,:) = 0

# # put frames around the slices
# [nr,nc,nd] = size(DSI)
# hold on
# for v=[100 200 300 400 500]
#     plot3([1 nc nc 1 1 ], v*[1 1 1 1 1], [1 1 nd nd 1], 'b', 'LineWidth', 1.5)
# end
# colormap(parula)

rvcprint.rvcprint()

