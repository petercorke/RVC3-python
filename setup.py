from setuptools import setup, find_packages, Extension
import os

# fmt: off
import pip
pip.main(['install', 'numpy>=1.17.4'])
import numpy
# fmt: on

here = os.path.abspath(os.path.dirname(__file__))

req = [
    "numpy>=1.17.4",
    "scipy",
    "matplotlib",
    "roboticstoolbox-python",
    "machinevision-toolbox-python",
]

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="RVC3-python",
    version="0.1.0",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://petercorke.github.io/RVC3-python",
        "Source": "https://github.com/petercorke/RVC3-python",
        "Tracker": "https://github.com/petercorke/RVC3-python/issues",
    },
    keywords="python robotics robot-manipulator mobile-robot computer-vision",
    packages=find_packages(exclude=["tests", "notebooks"]),
    # package_data={"roboticstoolbox": extra_files},
    scripts=["RVC3/bin/rvctool"],
    install_requires=req,
    extras_require={
    },
)
