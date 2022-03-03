# Robotics, Vision & Control 3rd edition in Python

This book depends on the following open-source Python packages:

- [Robotics Toolbox for Python](https://github.com/petercorke/robotics-toolbox-python)
- [Machine Vision Toolbox for Python](https://github.com/petercorke/machinevision-toolbox-python)

which in turn have dependencies on other packages created by the author and third parties.

This package provides a simple one-step installation of the Toolboxes
```
$ pip install rvc3book
```
or
```
$ conda install rvc3book
```

The package also provides other resources for readers including:

- rvctool, a command line script that is an IPython wrapper. It imports the
  above mentioned packages using `import *` and then provides an interactive
  computing environment.  By default `rvctool` has prompts like the regular
  Python REPL not IPython, and it automatically displays the results of
  expressions like MATLAB does - put a semicolon on the end of the line to
  suppress that.  `rvctool` allows cutting and pasting in lines from the book, and
  prompt characters are ignored.
- The complete code to produce every Python-generated figure in the book.
- All example scripts.
- All block diagram models.

Block diagram models are simulated using the Python package [bdsim](https://github.com/petercorke/bdsim) which can run models:

- written in Python using [bdsim](https://github.com/petercorke/bdsim#getting-started) blocks and wiring.
- created graphically using [bdedit](https://github.com/petercorke/bdsim#bdedit-the-graphical-editing-tool) and saved as a `.bd` (JSON format) file.
