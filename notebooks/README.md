# Python notebooks

The code for each chapter is available as Python notebook (.ipynb file) and these are available in
this [folder](.).  They can also be run, from GitHub, on [Google Colab](https://colab.research.google.com/?utm_source=scs-index) by clicking the Colab button below.

| Chapter | Topic | Open |
| ------- |------ | ---- |
| 2 | Representing position & orientation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap2.ipynb)
| 3 | Time & Motion | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap3.ipynb)
| **Mobile Robotics** |||
| 4 | Mobile Robot Vehicles | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap4.ipynb)
| 5 | Navigation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap5.ipynb)
| 6 | Localization & Mapping | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap6.ipynb)
| **Robot Manipulators** |||
| 7 | Robot Arm Kinematics | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap7.ipynb)
| 8 | Manipulator Velocity | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap8.ipynb)
| 9 | Dynamics & Control | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap9.ipynb)
| **Computer Vision** |||
| 10 | Light & Color | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap10.ipynb)
| 11 | Images & Image Processing | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap11.ipynb)
| 12 | Image Feature Extraction | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap12.ipynb)
| 13 | Image Formation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap13.ipynb)
| 14 | Using Multiple Images | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap14.ipynb)
| **Vision-Based Control** |||
| 15 | Vision-based Control | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap16.ipynb)
| 16 | Advanced Visual Servoing | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap16.ipynb)

# Animation issues

Matplotlib and Jupyter don't play as well together as they should.  The biggest issues are:
- ensuring that multiple plots that are meant to overlay appear on the one figure, not separate figures
- animations

The Jupyter code is annotated where this is an issue, and sometimes alternative appproaches are
given instead.

Animations using Matplotlib work well from the Python REPL or scripts, or from IPython (`rvctool`).
# Convert to Python script

To convert a Jupyter notebook to a Python script use
```shell
jupyter nbconvert notebook.ipynb --to python
```
which creates `notebook.py`

Other options for `--to` include `html`, `pdf`, `markdown`, `latex`.  See
```shell
jupyter nbconvert help
```
for all the details.