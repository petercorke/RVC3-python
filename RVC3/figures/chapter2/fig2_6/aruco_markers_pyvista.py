from pathlib import Path
import numpy as np
import cv2
import cv2.aruco as aruco
from spatialmath import SE3
import pyvista as pv
import pvplus


def main():
    marker_img_file =  Path('2021-08-25-Markers-1.png')
    background_img_file =  Path('2021-08-25-Markers-2.png')

    # marker_img_file =  Path('2021-08-25-Markers-HiRes-1.tif')
    # background_img_file =  Path('2021-08-25-Markers-HiRes-2.tif')

    marker_img = cv2.imread(str(marker_img_file))
    print("shape =", marker_img.shape)
    # background_img = cv2.imread(str(background_img_file))

    # if background_img.shape != marker_img.shape:
    #     print(f"Resizing background image to {(marker_img.shape[1], marker_img.shape[0])}")
    #     background_img = cv2.resize(background_img, (marker_img.shape[1], marker_img.shape[0]),
    #                                 interpolation=cv2.INTER_CUBIC)

    grey_img = cv2.cvtColor(marker_img, cv2.COLOR_BGR2GRAY)
    tag_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    aruco_params = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(grey_img, tag_dict, parameters=aruco_params)

    # camera matrix and distortion parameters
    ccd_width = 35.9
    focal_length = 35
    fx = (focal_length / ccd_width) * marker_img.shape[1]
    fy = fx
    cx = marker_img.shape[1] / 2
    cy = marker_img.shape[0] / 2
    camera_matrix = np.array([
        [fx, 0, cx],
        [0, fy, cy],
        [0, 0, 1]
    ])
    distortion = np.array([[0.0, 0.0, 0.0, 0.0, 0.0]])

    # Use the detected markers and the camera calibration to estimate the 3D pose
    rvecs, tvecs, corners = aruco.estimatePoseSingleMarkers(bboxs, 133 / 1000, camera_matrix, distortion)

    # Convert to SE3 poses
    poses = [
        # rvec is in the reduced Rodrigues format
        # see https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac
        SE3.Rt(cv2.Rodrigues(rvec)[0], tvec)
        for rvec, tvec in zip(rvecs, tvecs)
    ]
    # Sort by the x-position so that the ordering is consistent between runs
    poses = sorted(poses, key=lambda pose: pose.t[0])

    # adjustments to the frame positions in post
    corrections = [
        # Arm Base
        SE3.Ty(-0.1),
        # Robot base
        SE3.Rz(np.pi),
        # Gripper
        SE3.Tz(-0.05),
        # Target
        SE3(),
        # World
        SE3(),
        # Camera
        SE3.Ty(0.06),
    ]
    poses = [pose * corr for pose, corr in zip(poses, corrections)]

    # Draw the coordinate axes using pyvista
    print("shape =", marker_img.shape)
    plotter = pv.Plotter(polygon_smoothing=True,
                         window_size=(int(marker_img.shape[1]), int(marker_img.shape[0])))
    plotter.add_background_image(str(background_img_file))
    plotter.disable_parallel_projection()
    plotter.set_position([0, 0, 0])
    plotter.set_focus([0, 0, 1])
    plotter.set_viewup([0, -1, 0])
    desired_view_angle = 2 * np.arctan(cy / fy) * 180 / np.pi   # Pyvista view angle is the vertical view angle
    plotter.camera.zoom(plotter.camera.view_angle / desired_view_angle)
    print(f"Changed view angle to {plotter.camera.view_angle} (desired was {desired_view_angle})")
    print(f"Camera direction is forward {plotter.camera.direction}, up {plotter.camera.up}")
    print(f"Camera clipping is {plotter.camera.clipping_range}")
    for pose, name in zip(poses, ['B', 'M', 'E', 'W', '0', 'C']):
        print(name)
        pvplus.add_frame(plotter, pose, scale=0.2, label=name)

    # Add a light, for improved visibility
    light = pv.Light(light_type=pv.Light.SCENE_LIGHT, color=(1.0, 1.0, 1.0),
                     position=(0, -10, 0), focal_point=(0, 0, 0), intensity=2, positional=False)
    plotter.add_light(light)

    # plotter.show(screenshot=str(background_img_file.parent / f"{background_img_file.stem}-pyvista-axes.png"))
    plotter.show(screenshot=str(background_img_file.resolve().parent.parent / "Figures_generated" / "fig2_6.png"))


if __name__ == '__main__':
    main()
