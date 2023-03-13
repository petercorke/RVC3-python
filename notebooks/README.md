# Python notebooks

The code for each chapter is available as Python notebook (.ipynb file) and these are available in
this [folder](.).  They can also be run, from GitHub, on [Google Colab](https://colab.research.google.com/?utm_source=scs-index) by clicking the Colab button below.

| Chapter | Topic | Open |
| ------- |------ | ---- |
| **Foundations (Part I)** |||
| 2 | Representing position & orientation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap2.ipynb)
| 3 | Time & Motion | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap3.ipynb)
| **Mobile Robotics (Part II)** |||
| 4 | Mobile Robot Vehicles | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap4.ipynb)
| 5 | Navigation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap5.ipynb)
| 6 | Localization & Mapping | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap6.ipynb)
| **Robot Manipulators (Part III)** |||
| 7 | Robot Arm Kinematics | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap7.ipynb)
| 8 | Manipulator Velocity | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap8.ipynb)
| 9 | Dynamics & Control | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap9.ipynb)
| **Computer Vision (Part IV)** |||
| 10 | Light & Color | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap10.ipynb)
| 11 | Images & Image Processing | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap11.ipynb)
| 12 | Image Feature Extraction | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap12.ipynb)
| 13 | Image Formation | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap13.ipynb)
| 14 | Using Multiple Images | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap14.ipynb)
| **Vision-Based Control (Part V)** |||
| 15 | Vision-based Control | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap16.ipynb)
| 16 | Advanced Visual Servoing | [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/petercorke/RVC3-python/blob/main/notebooks/chap16.ipynb)


# Issues when running with CoLab

## Ancient Matplotlib

These notebooks work for > 3.6.0 and progressively less well for older versions.  CoLab is problematic because
it provides only 3.2.2 (as of January 2023) and are problems with some multi-stage plots not properly
overlaying, and ending up as a stack of individual plots.


Therefore the first code cell in the notebook installs a newer version of Matplotlib.  This is an annoying thing to have to
do, since then we have to restart the kernel and run the cell again.  Until Google updates the default
Matplotlib I'm not sure what else to do.

##  Animation issues

Animations using Matplotlib work well from the Python REPL or scripts, or from IPython (`rvctool`).

I have not found a good way to do Matplotlib animations from CoLab.  Jupyter itself makes this hard
but you can always have windows that pop out of Jupyter, this can't be done from CoLab.

The Jupyter code is annotated where this is an issue, and sometimes alternative appproaches are
given instead.


## Setting default result printing

The book assumes that Python results are displayed by default, and use a semicolon on the end of the
line to disable the printing.  This is like MATLAB and simplifies the examples, print statements are
not required.  In a Jupyter this automatic printing only applies to the last statement in the cell.

This feature is enabled in the first code cell of the notebook with the code lines:

```
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "last_expr_or_assign"
```

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