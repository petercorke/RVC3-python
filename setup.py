from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

req = [
    "matplotlib",
    "roboticstoolbox-python >= 1",
    "machinevision-toolbox-python",
    "bdsim",
    "IPython",
    "sympy",
]

pytorch_req = [
    "torch",
    "torchvision",
]

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rvc3python",
    version="0.2.2",
    description="Support for book: Robotics, Vision & Control 3 in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petercorke/RVC3-python",
    author="Peter Corke",
    license="MIT",
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://petercorke.github.io/RVC3-python",
        "Source": "https://github.com/petercorke/RVC3-python",
        "Tracker": "https://github.com/petercorke/RVC3-python/issues",
    },
    keywords=["robotics", "robot", "manipulator", "robot arm", 
        "mobile robot", "mobile manipulation",
        "path planning", "SLAM", "pose graph", 
        "Dubins", "Reeds-Shepp", "lattice planner", "RRT", "PRM",
        "rapidly exploring random tree", "probabilistic roadmap planner",
        "force control", "kinematics", "Jacobian", "position control", "velocity control",
        "spatial math", 
        "SO(2)", "SE(2)", "SO(3)", "SE(3)",
        "twist", "product of exponential", "translation", "orientation",
        "angle-axis", "Lie group", "skew symmetric matrix",
        "pose", "translation", "rotation matrix", "rigid body transform", "homogeneous transformation",
        "Euler angles", "roll-pitch-yaw angles", "quaternion", "unit-quaternion"
        "computer vision", "machine vision", "robotic vision",
        "color space", "blackbody", "image segmentation", "blobs",
        "Hough transform", "k-means", "homography", "camera calibration", "visual odometry",
        "bundle adjustment",  "stereo vision", "rectification"
        ],
    #packages=["RVC3"],
    packages=find_packages(),
    # package_data={"roboticstoolbox": extra_files},
    # include_package_data=False,
    scripts=["RVC3/bin/rvctool", "RVC3/bin/bdsim_path"],
    install_requires=req,
    extras_require={
            "pytorch": pytorch_req,
    },
)
