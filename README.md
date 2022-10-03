# Robotics, Vision & Control: 3rd edition in Python

THIS IS A PLACEHOLDER.  THE BOOK WILL BE PUBLISHED LATE IN 2022. THIS REPO IS A WIP UNTIL THEN

<img src="https://github.com/petercorke/RVC3-python/raw/main/figs/frontcover.png" alt="Front cover 978-3-031-06468-5_5208" width="300">


This book depends on the following open-source Python packages:

- [Robotics Toolbox for Python](https://github.com/petercorke/robotics-toolbox-python)
- [Machine Vision Toolbox for Python](https://github.com/petercorke/machinevision-toolbox-python)

which in turn have dependencies on other packages created by the author and third parties.

This package provides a simple one-step installation of the required Toolboxes
```
$ pip install rvc3python
```
or
```
$ conda install rvc3python
```

The package also provides other resources for readers including:

- Command line executable tools include:
  - `rvctool`, a command line script that is an IPython wrapper. It imports the
    above mentioned packages using `import *` and then provides an interactive
    computing environment.  By default `rvctool` has prompts like the regular
    Python REPL not IPython, and it automatically displays the results of
    expressions like MATLAB does - put a semicolon on the end of the line to
    suppress that.  `rvctool` allows cutting and pasting in lines from the book, and
    prompt characters are ignored.
  - `eigdemo`, animation showing linear transformation of rotating unit vector
  - `tripleangledemo`, experiment with various triple-angle sequences
  - `twistdemo`, experiment with 3D twists

- The complete code to produce every Python-generated figure in the book, see folder `figures`
- All example scripts, see folder `examples`
- All block diagram models, see folder `models`

Block diagram models are simulated using the Python package [bdsim](https://github.com/petercorke/bdsim) which can run models:

- written in Python using [bdsim](https://github.com/petercorke/bdsim#getting-started) blocks and wiring.
- created graphically using [bdedit](https://github.com/petercorke/bdsim#bdedit-the-graphical-editing-tool) and saved as a `.bd` (JSON format) file.

```
 ____       _           _   _             __     ___     _                ___      ____            _             _   _____ 
|  _ \ ___ | |__   ___ | |_(_) ___ ___    \ \   / (_)___(_) ___  _ __    ( _ )    / ___|___  _ __ | |_ _ __ ___ | | |___ / 
| |_) / _ \| '_ \ / _ \| __| |/ __/ __|    \ \ / /| / __| |/ _ \| '_ \   / _ \/\ | |   / _ \| '_ \| __| '__/ _ \| |   |_ \ 
|  _ < (_) | |_) | (_) | |_| | (__\__ \_    \ V / | \__ \ | (_) | | | | | (_>  < | |__| (_) | | | | |_| | | (_) | |  ___) |
|_| \_\___/|_.__/ \___/ \__|_|\___|___( )    \_/  |_|___/_|\___/|_| |_|  \___/\/  \____\___/|_| |_|\__|_|  \___/|_| |____/ 
                                      |/                                                                                   
for Python (RTB==0.11.0, MVTB==0.5.5, SMTB==0.11.0)

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from math import pi
from spatialmath import *
from spatialmath.base import *
from roboticstoolbox import *
from machinevisiontoolbox import *
import machinevisiontoolbox.base as mvbase

func/object?       - show brief help
help(func/object)  - show detailed help
func/object??      - show source code


Results of assignments will be displayed, use trailing ; to suppress

 
Python 3.8.5 (default, Sep  4 2020, 02:22:02) 
Type 'copyright', 'credits' or 'license' for more information
IPython 8.0.1 -- An enhanced Interactive Python. Type '?' for help.


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

>>> 
```
