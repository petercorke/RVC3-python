# Recorded script from Mayavi2
from numpy import array
try:
    engine = mayavi.engine
except NameError:
    from mayavi.api import Engine
    engine = Engine()
    engine.start()
if len(engine.scenes) == 0:
    engine.new_scene()
# ------------------------------------------- 
module_manager3 = engine.scenes[0].children[3].children[0]
module_manager3.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager3.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager3.scalar_lut_manager.scalar_bar_representation.position = array([0.82, 0.1 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.position2 = array([0.17, 0.8 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.place_factor = 0.19357500000000002
module_manager3.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager3.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager3.scalar_lut_manager.scalar_bar_representation.position = array([0.82, 0.1 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.position2 = array([0.17, 0.8 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.place_factor = 0.01
module_manager3.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager3.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager3.scalar_lut_manager.scalar_bar_representation.position = array([0.82, 0.1 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.position2 = array([0.17, 0.8 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.place_factor = 10.5
module_manager3.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager3.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager3.scalar_lut_manager.scalar_bar_representation.position = array([0.82, 0.1 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.position2 = array([0.17, 0.8 ])
module_manager3.scalar_lut_manager.scalar_bar_representation.place_factor = 0.5
axes = engine.scenes[0].children[4].children[0].children[1]
axes.label_text_property.shadow_offset = array([ 1, -1])
axes.label_text_property.bold = False
axes.label_text_property.shadow_offset = array([ 1, -1])
axes.label_text_property.font_size = 8
axes.title_text_property.shadow_offset = array([ 1, -1])
axes.title_text_property.bold = False
axes.title_text_property.shadow_offset = array([ 1, -1])
axes.title_text_property.bold = True
axes.title_text_property.shadow_offset = array([ 1, -1])
axes.title_text_property.bold = False
axes.title_text_property.shadow_offset = array([ 1, -1])
axes.title_text_property.font_size = 8
module_manager4 = engine.scenes[0].children[4].children[0]
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.17, 0.8 ])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
scene = engine.scenes[0]
scene.scene.camera.position = [1328.7774523276864, 1152.16267299122, 596.2759992356562]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.2968781540332323, -0.2516414526803261, 0.921162277207852]
scene.scene.camera.clipping_range = [651.7458314343656, 2465.5587760103754]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1385.4835948606305, 1032.3252392121817, 646.7558688853404]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3276326027227163, -0.27269770632141305, 0.9045954004969179]
scene.scene.camera.clipping_range = [680.0604403402217, 2428.1692883492206]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1385.4835948606305, 1032.3252392121817, 646.7558688853404]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [680.0604403402217, 2428.1692883492206]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1621.6251497813632, 1181.38853944674, 777.219601351262]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [985.204533411526, 2741.019040336467]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1907.3564312354497, 1361.7551327305555, 935.0807176350272]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [1354.4288860278048, 3119.5672402410346]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1621.6251497813632, 1181.3885394467397, 777.219601351262]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [985.204533411526, 2741.019040336467]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1385.4835948606305, 1032.3252392121815, 646.7558688853404]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [680.0604403402217, 2428.1692883492206]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1190.3252850087854, 909.1324291009763, 538.9346023845787]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3627537265029343, -0.21825872931849202, 0.9059651543986179]
scene.scene.camera.clipping_range = [427.87523945484674, 2169.615774310174]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
scene.scene.camera.position = [1173.485170290038, 894.8394829909678, 583.3499021831709]
scene.scene.camera.focal_point = [261.0, 322.5, 25.5]
scene.scene.camera.view_angle = 30.0
scene.scene.camera.view_up = [-0.3936322021725195, -0.2379005029285883, 0.8879510347531203]
scene.scene.camera.clipping_range = [441.614360447841, 2152.948893224912]
scene.scene.camera.compute_view_plane_normal()
scene.scene.render()
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.use_bounds = False
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.use_bounds = True
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.handle_size = 10.01
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.handle_size = 100.1
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.handle_size = 10.01
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.handle_size = 10.0
module_manager4.scalar_lut_manager.scalar_bar_representation.show_border = 'off'
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.show_horizontal_border = 0
module_manager4.scalar_lut_manager.scalar_bar_representation.show_border = 'active'
module_manager4.scalar_lut_manager.scalar_bar_representation.maximum_size = array([100000, 100000])
module_manager4.scalar_lut_manager.scalar_bar_representation.minimum_size = array([1, 1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.1])
module_manager4.scalar_lut_manager.scalar_bar_representation.position2 = array([0.5, 0.8])
module_manager4.scalar_lut_manager.scalar_bar_representation.show_horizontal_border = 2
