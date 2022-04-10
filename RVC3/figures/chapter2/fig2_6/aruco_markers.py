from pathlib import Path
import numpy as np
import cv2
import cv2.aruco as aruco
from spatialmath import SE3, SO3
import pyvista as pv
import pvplus


def main():
    marker_img_file = Path(__file__).parent / 'marker_imgs' / '2021-08-25-Markers-HiRes-1.tif'
    background_img_file = Path(__file__).parent / 'marker_imgs' / '2021-08-25-Markers-HiRes-2.tif'
    marker_img = cv2.imread(str(marker_img_file))
    background_img = cv2.imread(str(background_img_file))

    if background_img.shape != marker_img.shape:
        print(f"Resizing background image to {(marker_img.shape[1], marker_img.shape[0])}")
        background_img = cv2.resize(background_img, (marker_img.shape[1], marker_img.shape[0]),
                                    interpolation=cv2.INTER_CUBIC)

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

    img = background_img
    for pose in poses:
        img = cv2.drawFrameAxes(img, camera_matrix, distortion, pose.R, pose.t, 0.25, 25)

    cv2.imwrite(str(background_img_file.parent / f"{background_img_file.stem}-axes.png"), img)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()
