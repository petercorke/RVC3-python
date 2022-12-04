import math
import pyvista as pv
import numpy as np
from pathlib import Path
from spatialmath import SE3
from pyvista.utilities.fileio import standard_reader_routine
from vtkmodules.vtkIOImport import vtkGLTFImporter


# A transform between the default glTF coordinate frame, and the pyvista frame.
import pvplus

GLTF_FRAME = SE3(np.array([
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
]))


def read_gltf(filename: str):
    """
    Load a glTF model from file into a pyvista object.
    Based on the program flow in pyvista.fileio.read.
    As far as I can tell, vtkGLTFReader could be added to READERS in pyvista.fileio,
    and everything will just work, but it needs testing.

    :param filename: The filename to load from
    :return: A pyvista data object, for glTF, will always be a pyvista MultiBlock, due to the scene structure.
    """
    from vtkmodules.vtkIOGeometry import vtkGLTFReader
    reader = vtkGLTFReader()
    return standard_reader_routine(reader, str(filename))


def plot_multicolour_mesh(
        plotter: pv.Plotter,
        mesh: pv.MultiBlock,
        coordinate_frame: SE3 = None,
        name: str = None,
        colour_array: str = 'BaseColorMultiplier',
        metallic_roughness_array: str = 'MetallicRoughness',
        **kwargs):
    """
    Plot a mesh with colour information imported from a glTF file.
    The scene structure of glTF files seems to always create nested
    VTK loads triangles with different colours as separate PolyData objects within the MultiBlock.
    Colour and material information is stored in array properties on the PolyData object,
    which is used to determine the rendering properties.

    The code here is copied from the MultiBlock handling section of pyvista.plotting.add_mesh.

    :param plotter: The plotter object
    :param mesh: The mesh to plot. Based on GLTF, this should always be a pv.MultiBlock
    :param coordinate_frame: A transformation to apply to all the rendered meshes.
    :param name: The base name of the object. Actual meshes will have indices appended to this, as '{name}-0', etc.
    :param colour_array: The name of the array to read colour information from.
    :param metallic_roughness_array: The name of the array to read metallic and roughness info from.
    :param kwargs: Additional arguments that are passed through to plotter.add_mesh
    :return: A list of newly created actors
    """
    # Choose a default name
    if name is None:
        name = f'{type(mesh).__name__}({mesh.memory_address})'
    if coordinate_frame is None:
        coordinate_frame = SE3()
    # Account for the glTF frame
    coordinate_frame = coordinate_frame * GLTF_FRAME

    # Now iteratively plot each element of the MultiBlock dataset
    # Nested MultiBlock are expanded, rather than
    actors = []
    data_to_add = [mesh]
    while len(data_to_add) > 0:
        dataset = data_to_add.pop(0)
        for idx in range(dataset.GetNumberOfBlocks()):
            if dataset[idx] is None:
                continue

            # Get the data object
            if not pv.is_pyvista_dataset(dataset[idx]):
                data = pv.wrap(dataset.GetBlock(idx))
                if not pv.is_pyvista_dataset(dataset[idx]):
                    continue  # move on if we can't plot it
            else:
                data = dataset.GetBlock(idx)
            if data is None or (not isinstance(data, pv.MultiBlock) and data.n_points < 1):
                # Note that a block can exist but be None type
                # or it could have zeros points (be empty) after filtering
                continue

            if isinstance(data, pv.MultiBlock):
                # This is another multiblock, add it to the queue
                data_to_add.append(data)
            else:
                # Get a good name to use
                next_name = f'{name}-{len(actors)}'

                # Read colour information
                colour = pv.get_array(data, colour_array)
                # This is specified for gltf files, using the B channel for metal, and G channel for roughness
                # See: https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/schema/material.pbrMetallicRoughness.schema.json
                metallic_roughness = pv.get_array(data, metallic_roughness_array)

                # Add to the scene
                the_arguments = kwargs.copy()
                the_arguments['color'] = colour[0, 0:3]
                the_arguments['pbr'] = True
                the_arguments['name'] = next_name
                the_arguments['metallic'] = metallic_roughness[0, 1]
                the_arguments['roughness'] = metallic_roughness[0, 2]
                data.transform(coordinate_frame.A)
                a = plotter.add_mesh(data, **the_arguments)
                actors.append(a)
    return actors


def draw_puma(
        plotter: pv.Plotter,
        model_dir: Path,
        joint1_angle: float = 0.0,
        joint2_angle: float = 0.0,
        joint3_angle: float = 0.0,
        joint4_angle: float = 0.0,
        joint5_angle: float = 0.0,
        base_transform: SE3 = None,
        name: str = 'Puma560'
):
    """
    Render a Puma 560 arm, with certain joint angles, to the given plotter.
    Models are loaded from the given model dir.

    :param plotter: The plotter to plot to
    :param model_dir: A directory containing the required glb files.
    :param joint1_angle: The angle of the first joint rotating around Z, in radians
    :param joint2_angle: The angle of the first elevating shoulder, in radians
    :param joint3_angle: The angle of the elbow joint, in radians. There is a default 90 degree bend at the elbow
    :param joint4_angle: The angle of the wrist joint, in radians.
    :param joint5_angle: The angle of the end effector, in radians.
    :param base_transform: The location to draw the base, affecting the position of all parts.
    :param name: The name of the plotted actors. Use the same name to replace existing.
    Actual actor names will include the link number and actor number within
    :return: A list of 6 lists of actors, corresponding to the 6 arm links.
    Some links are represented by more than one actor, which are grouped into the sub-lists.
    """
    if base_transform is None:
        base_transform = SE3()

    actors = []

    part = read_gltf(str(model_dir / 'Puma560_link1.glb'))
    a = plot_multicolour_mesh(plotter, part, base_transform, name=f"{name}-link1")
    actors.append(a)

    j1_pose = base_transform * SE3(0, 0, 0.62357) * SE3.Rz(joint1_angle)

    part2_pose = j1_pose * SE3(0, 0, 0.00)
    part = read_gltf(str(model_dir / 'Puma560_link2.glb'))
    a = plot_multicolour_mesh(plotter, part, part2_pose, name=f"{name}-link2")
    actors.append(a)

    j2_pose = part2_pose * SE3(0, -0.16764, 0) * SE3.Ry(-joint2_angle)  # the reference has positive angles elevating

    part3_pose = j2_pose * SE3(0.0, 0.0, 0.0)
    part = read_gltf(str(model_dir / 'Puma560_link3.glb'))
    a = plot_multicolour_mesh(plotter, part, part3_pose, name=f"{name}-link3")
    actors.append(a)

    j3_pose = part3_pose * SE3(0.4318, 0, 0) * SE3.Ry(np.pi - joint3_angle)

    part4_pose = j3_pose * SE3(0.0, 0.0, 0.0)
    part = read_gltf(str(model_dir / 'Puma560_link4.glb'))
    a = plot_multicolour_mesh(plotter, part, part4_pose, name=f"{name}-link4")
    actors.append(a)

    j4_pose = part4_pose * SE3(0.0, 0.0381, -0.35179) * SE3.Rz(-np.pi / 2 - joint4_angle)

    part5_pose = j4_pose * SE3(0.0, 0.0, -0.02032)
    part = read_gltf(str(model_dir / 'Puma560_link5.glb'))
    a = plot_multicolour_mesh(plotter, part, part5_pose, name=f"{name}-link5")
    actors.append(a)

    j5_pose = part5_pose * SE3(0, 0, -0.059979) * \
              SE3.Rz(math.radians(90)) * SE3.Ry(np.pi / 2 - joint5_angle)

    part6_pose = j5_pose * SE3(0.0, 0.0, 0.0)
    part = read_gltf(str(model_dir / 'Puma560_link6.glb'))
    a = plot_multicolour_mesh(plotter, part, part6_pose, name=f"{name}-link6")
    actors.append(a)

    return actors


def main():
    plotter = pv.Plotter(polygon_smoothing=True, window_size=(2000, 2000))
    plotter.disable_parallel_projection()

    

    model_dir = Path(__file__).parent / 'models'
    # qz:
    # draw_puma(
    #     plotter=plotter,
    #     model_dir=model_dir,
    #     joint1_angle=math.radians(0),
    #     joint2_angle=math.radians(0),
    #     joint3_angle=math.radians(0),
    #     joint4_angle=math.radians(0),
    #     joint5_angle=math.radians(0),
    #     base_transform=SE3.Rz(math.radians(135))
    # )
    # lu:
    # This one does not match the diagram, but is a plausible "left, elbow-up" pose.
    # The given reference diagram is identical to 'ru', which seems like an error.
    draw_puma(
        plotter=plotter,
        model_dir=model_dir,
        joint1_angle=2.6486,
        joint2_angle=-3.9270,
        joint3_angle=0.0940,
        joint4_angle=2.5326,
        joint5_angle=0.9743,
        base_transform=SE3.Rz(math.radians(135))
    )
    # ld:
    # draw_puma(
    #     plotter=plotter,
    #     model_dir=model_dir,
    #     joint1_angle=2.6486,
    #     joint2_angle=-2.3081,
    #     joint3_angle=3.1416,
    #     joint4_angle=0.6743,
    #     joint5_angle=0.8604,
    #     base_transform=SE3.Rz(math.radians(135))
    # )
    # ru:
    # draw_puma(
    #     plotter=plotter,
    #     model_dir=model_dir,
    #     joint1_angle=-0,
    #     joint2_angle=0.7854,
    #     joint3_angle=3.1416,
    #     joint4_angle=-0,
    #     joint5_angle=0.7854,
    #     base_transform=SE3.Rz(math.radians(135))
    # )
    # rd:
    # draw_puma(
    #     plotter=plotter,
    #     model_dir=model_dir,
    #     joint1_angle=0,
    #     joint2_angle=-0.8335,
    #     joint3_angle=0.0940,
    #     joint4_angle=-3.1416,
    #     joint5_angle=0.8312,
    #     base_transform=SE3.Rz(math.radians(135))
    # )

    plotter.set_background('white')
    # pvplus.export_gltf(plotter, 'example-puma.glb')
    plotter.show(screenshot='fig3_1b.png')


if __name__ == '__main__':
    main()
