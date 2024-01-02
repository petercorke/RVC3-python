# Robotics, Vision & Control: 3rd edition in Python (2023)
[![A Python Robotics Package](https://raw.githubusercontent.com/petercorke/robotics-toolbox-python/master/.github/svg/py_collection.min.svg)](https://github.com/petercorke/robotics-toolbox-python)
[![QUT Centre for Robotics Open Source](https://github.com/qcr/qcr.github.io/raw/master/misc/badge.svg)](https://qcr.github.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![PyPI version](https://badge.fury.io/py/rvc3python.svg)](https://badge.fury.io/py/rvc3python)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rvc3python.svg)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/rvc3python)](https://pypistats.org/packages/rvc3python)

<table style="border:0px">
<tr style="border:0px">
<td style="border:0px">
<img src="https://github.com/petercorke/RVC3-python/raw/main/doc/frontcover.png" alt="Front cover 978-3-031-06468-5_5208" width="300">
</td>
<td style="border:0px">
Welcome to the online hub for the book:
<ul type="none">
<li><b>Robotics, Vision & Control</b>: fundamental algorithms in Python (3rd edition) 
<li>Peter Corke, published by Springer-Nature 2023.</li>
<li><b>ISBN</b> 978-3-031-06468-5 (hardcopy), 978-3-031-06469-2 (eBook)</li>
<li><b>DOI</b> <a href="https://doi.org/10.1007/978-3-031-06469-2">10.1007/978-3-031-06469-2</a></li>
</ul>
<br><br>
<p>Report an issue with the book or its supporting code <a href="https://github.com/petercorke/RVC3-python/issues/new/choose">here</a>.</p>

<p>Known errata for the book can be viewed <a href="https://github.com/petercorke/RVC3-python/wiki/Errata">here</a>.</p>
</td>
</tr>
</table>


This book uses many examples based on the following open-source Python packages

<a href="https://github.com/petercorke/robotics-toolbox-python"><img alt="Robotics Toolbox for Python" src="https://github.com/petercorke/robotics-toolbox-python/raw/master/docs/figs/RobToolBox_RoundLogoB.png" width="130"></a>
<a href="https://github.com/petercorke/machinevision-toolbox-python"><img alt="Machine Vision Toolbox for Python" src="https://github.com/petercorke/machinevision-toolbox-python/raw/master/figs/VisionToolboxLogo_NoBackgnd@2x.png" width="150"></a>
<a href="https://github.com/petercorke/spatialmath-python"><img alt="Spatial Maths Toolbox for Python" src="https://github.com/petercorke/spatialmath-python/raw/master/docs/figs/CartesianSnakes_LogoW.png" width="130"></a>
<a href="https://github.com/petercorke/bdsim"><img alt="Block diagram simulation for Python" src="https://github.com/petercorke/bdsim/raw/master/figs/BDSimLogo_NoBackgnd@2x.png" width="250"></a>

**Robotics Toolbox for Python**, **Machine Vision Toolbox for Python**, **Spatial Maths Toolbox for Python**, **Block Diagram Simulation for Python**.  These in turn have dependencies on other packages created by the author and
third parties.

## Installing the package

This package provides a simple one-step installation of *all* the required Toolboxes
```shell
pip install rvc3python
```
or
```shell
conda install rvc3python
```

There are a lot of dependencies and this might take a minute or so.  You now have a very
powerful computing environment for robotics and computer vision.

### Python version

Given the rapid rate of language additions, particularly around type hinting, use at
least Python 3.8.  Python 3.7 goes end of life in June 2023.

Not all package dependencies will work with the latest release of Python.  In particular, check:
* [PyTorch](https://pypi.org/project/torch/) used for segmentation examples in Chapter 12
* [Open3D](https://pypi.org/project/open3d), used for point cloud examples in Chapter 14.

### Installing into a Conda environment

It's probably a good idea to create a virtual environment to keep this package
and its dependencies separated from your other Python code and projects.  If you've
never used virtual environments before this might be a good time to start, and it
is really easy [using Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html):
```shell
conda create -n RVC3 python=3.10
conda activate RVC3
pip install rvc3python
```

### Installing deep learning tools

Chapter 11 has some deep learning examples based on PyTorch.  If you don't have 
PyTorch installed you can use the `pytorch` install option
```shell
pip install rvc3python[pytorch]
```
or
```shell
conda install rvc3python
```
## Using the Toolboxes

The simplest way to get going is to use the command line tool

```shell
$ rvctool
 ____       _           _   _             __     ___     _                ___      ____            _             _   _____ 
|  _ \ ___ | |__   ___ | |_(_) ___ ___    \ \   / (_)___(_) ___  _ __    ( _ )    / ___|___  _ __ | |_ _ __ ___ | | |___ / 
| |_) / _ \| '_ \ / _ \| __| |/ __/ __|    \ \ / /| / __| |/ _ \| '_ \   / _ \/\ | |   / _ \| '_ \| __| '__/ _ \| |   |_ \ 
|  _ < (_) | |_) | (_) | |_| | (__\__ \_    \ V / | \__ \ | (_) | | | | | (_>  < | |__| (_) | | | | |_| | | (_) | |  ___) |
|_| \_\___/|_.__/ \___/ \__|_|\___|___( )    \_/  |_|___/_|\___/|_| |_|  \___/\/  \____\___/|_| |_|\__|_|  \___/|_| |____/ 
                                      |/                                                                                   
                                                                                 
for Python (RTB==1.1.0, MVTB==0.9.5, SG==1.1.7, SMTB==1.1.7, NumPy==1.24.2, SciPy==1.10.1, Matplotlib==3.7.1)

    import math
    import numpy as np
    from scipy import linalg, optimize
    import matplotlib.pyplot as plt
    from spatialmath import *
    from spatialmath.base import *
    from spatialmath.base import sym
    from spatialgeometry import *
    from roboticstoolbox import *
    from machinevisiontoolbox import *
    import machinevisiontoolbox.base as mvb
    
    # useful variables
    from math import pi
    puma = models.DH.Puma560()
    panda = models.DH.Panda()

    func/object?       - show brief help
    help(func/object)  - show detailed help
    func/object??      - show source code

Results of assignments will be displayed, use trailing ; to suppress
    
Python 3.10.9 | packaged by conda-forge | (main, Feb  2 2023, 20:24:27) [Clang 14.0.6 ]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.11.0 -- An enhanced Interactive Python. Type '?' for help.


>>> 
```

This provides an interactive Python
([IPython](https://ipython.readthedocs.io/en/stable)) session with all the Toolboxes and
supporting packages imported, and ready to go.  It's a highly capable, convenient, and
"MATLAB-like" workbench environment for robotics and computer vision.

For example to load an ETS model of a Panda robot, solve a forward kinematics
and inverse kinematics problem, and an interactive graphical display is simply:

```python
>>> panda = models.ETS.Panda()
ERobot: Panda (by Franka Emika), 7 joints (RRRRRRR)
┌─────┬───────┬───────┬────────┬─────────────────────────────────────────────┐
│link │ link  │ joint │ parent │             ETS: parent to link             │
├─────┼───────┼───────┼────────┼─────────────────────────────────────────────┤
│   0 │ link0 │     0 │ BASE   │ tz(0.333) ⊕ Rz(q0)                          │
│   1 │ link1 │     1 │ link0  │ Rx(-90°) ⊕ Rz(q1)                           │
│   2 │ link2 │     2 │ link1  │ Rx(90°) ⊕ tz(0.316) ⊕ Rz(q2)                │
│   3 │ link3 │     3 │ link2  │ tx(0.0825) ⊕ Rx(90°) ⊕ Rz(q3)               │
│   4 │ link4 │     4 │ link3  │ tx(-0.0825) ⊕ Rx(-90°) ⊕ tz(0.384) ⊕ Rz(q4) │
│   5 │ link5 │     5 │ link4  │ Rx(90°) ⊕ Rz(q5)                            │
│   6 │ link6 │     6 │ link5  │ tx(0.088) ⊕ Rx(90°) ⊕ tz(0.107) ⊕ Rz(q6)    │
│   7 │ @ee   │       │ link6  │ tz(0.103) ⊕ Rz(-45°)                        │
└─────┴───────┴───────┴────────┴─────────────────────────────────────────────┘

┌─────┬─────┬────────┬─────┬───────┬─────┬───────┬──────┐
│name │ q0  │ q1     │ q2  │ q3    │ q4  │ q5    │ q6   │
├─────┼─────┼────────┼─────┼───────┼─────┼───────┼──────┤
│  qr │  0° │ -17.2° │  0° │ -126° │  0° │  115° │  45° │
│  qz │  0° │  0°    │  0° │  0°   │  0° │  0°   │  0°  │
└─────┴─────┴────────┴─────┴───────┴─────┴───────┴──────┘

>>> panda.fkine(panda.qz)
   0.7071    0.7071    0         0.088     
   0.7071   -0.7071    0         0         
   0         0        -1         0.823     
   0         0         0         1      
>>> panda.ikine_LM(SE3.Trans(0.4, 0.5, 0.2) * SE3.Ry(pi/2))
IKSolution(q=array([  -1.849,   -2.576,   -2.914,     1.22,   -1.587,    2.056,   -1.013]), success=True, iterations=13, searches=1, residual=3.3549072615799585e-10, reason='Success')
>>> panda.teach(panda.qz)
```
![](https://github.com/petercorke/RVC3-python/raw/main/doc/panda_noodle.png)

Computer vision is just as easy.  For example, we can import an image, blur it
and display it alongside the original
```python
>>> mona = Image.Read("monalisa.png")
>>> Image.Hstack([mona, mona.smooth(sigma=5)]).disp()
```
![](https://github.com/petercorke/machinevision-toolbox-python/raw/master/figs/mona%2Bsmooth.png)

or load two images of the same scene, compute SIFT features and display putative
matches
```python
>>> sf1 = Image.Read("eiffel-1.png", mono=True).SIFT()
>>> sf2 = Image.Read("eiffel-2.png", mono=True).SIFT()
>>> matches = sf1.match(sf2)
>>> matches.subset(100).plot("w")
```
![](https://github.com/petercorke/machinevision-toolbox-python/raw/master/figs/matching.png)

`rvctool` is a wrapper around
[IPython](https://ipython.readthedocs.io/en/stable) where:
- robotics and vision functions and classes can be accessed without needing
  package prefixes
- results are displayed by default like MATLAB does, and like MATLAB you need to
  put a semicolon on the end of the line to prevent this
- the prompt is the standard Python REPL prompt `>>>` rather than the IPython
  prompt, this can be overridden by a command-line switch
- allows cutting and pasting in lines from the book, and prompt characters are
  ignored

The Robotics, Vision & Control book uses `rvctool` for all the included
examples.

`rvctool` imports the all the above mentioned packages using `import *` which is
not considered best Python practice.  It is very convenient for interactive
experimentation, but in your own code you can handle the imports as you see
fit.

### Cutting and pasting

IPython is very forgiving when it comes to cutting and pasting in blocks of Python
code.  It will strip off the `>>>` prompt character and ignore indentation.  The normal
python REPL is not so forgiving.  IPython also maintains a command history and
allows command editing.
### Simple scripting
You can write very simple scripts, for example `test.py` is

```python
T = puma.fkine(puma.qn)
sol = puma.ikine_LM(T)
sol.q
puma.plot(sol.q);
```

then 

```shell
$ rvctool test.py
   0         0         1         0.5963    
   0         1         0        -0.1501    
  -1         0         0         0.6575    
   0         0         0         1         

IKSolution(q=array([7.235e-08,  -0.8335,  0.09396,    3.142,   0.8312,   -3.142]), success=True, iterations=15, searches=1, residual=1.406125546650288e-07, reason='Success')
array([7.235e-08,  -0.8335,  0.09396,    3.142,   0.8312,   -3.142])
PyPlot3D backend, t = 0.05, scene:
  robot: Text(0.0, 0.0, 'Puma 560')
>>>
```
and you are dropped into an IPython session after the script has run.

## Issues running on Apple Silicon

Check out the [wiki page](https://github.com/petercorke/RVC3-python/wiki/Running-on-Apple-Silicon).

## Using Jupyter and Colab

Graphics and animations are problematic in these environments, some things work
well, some don't.  As much as possible I've tweaked the Jupyter notebooks to work
as best they can in these environments.

For local use the [Jupyter plugin for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) is pretty decent.  Colab suffers
from old versions of major packages (though they are getting better at keeping up to date)
and animations can suffer from slow update over the network.
## Other command line tools

Additional command line tools available (from the Robotics Toolbox) include:
- `eigdemo`, animation showing linear transformation of a rotating unit vector
  which demonstrates eigenvalues and eigenvectors.
- `tripleangledemo`, Swift visualization that lets you experiment with various triple-angle sequences.
- `twistdemo`, Swift visualization that lets you experiment with 3D twists. The screw axis is the blue rod and you can
   position and orient it using the sliders, and adjust its pitch. Then apply a rotation
   about the screw using the bottom slider.
# Block diagram models

<a href="https://github.com/petercorke/bdsim"><img
src="https://github.com/petercorke/bdsim/raw/master/figs/BDSimLogo_NoBackgnd%402x.png"
alt="bdsim logo" width="300"></a>

Block diagram models are key to the pedagogy of the RVC3 book and 25 models are
included. To simulate these models we use the Python package
[bdsim](https://github.com/petercorke/bdsim) which can run models:

- written in Python using
  [bdsim](https://github.com/petercorke/bdsim#getting-started) blocks and
  wiring.
- created graphically using
  [bdedit](https://github.com/petercorke/bdsim#bdedit-the-graphical-editing-tool)
  and saved as a `.bd` (JSON format) file.

The models are included in the `RVC3` package when it is installed and `rvctool`
adds them to the module search path.  This means you can invoke them from
`rvctool` by
```python
>>> %run -m vloop_test
```

If you want to directly access the folder containing the models, the command
line tool
```shell
bdsim_path
```
will display the full path to where they have been installed in the Python
package tree.


# Additional book resources

<img src="https://github.com/petercorke/RVC3-python/raw/main/doc/frontcover.png" alt="Front cover 978-3-031-06468-5_5208" width="100">

This GitHub repo provides additional resources for readers including:
- Jupyter notebooks containing all code lines from each chapter, see
  the [`notebooks`](notebooks) folder
- The code to produce every Python/Matplotlib (2D) figure in the book, see the [`figures`](figures) folder
- 3D points clouds from chapter 14, and the code to create them, see
  the [`pointclouds`](../pointclouds) folder.
- 3D figures from chapters 2-3, 7-9, and the code to create them, see the [`3dfigures`](../3dfigures) folder.
- All example scripts, see the [`examples`](examples) folder.
- To run the visual odometry example in Sect. 14.8.3 you need to download two image sequence, each over 100MB, [see the instructions here](https://github.com/petercorke/machinevision-toolbox-python/blob/master/mvtb-data/README.md#install-big-image-files). 

To get that material you must clone the repo
```shell
git clone https://github.com/petercorke/RVC3-python.git
```
