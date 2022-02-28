# bdsim models

This folder holds a number of [bdsim](https://github.com/petercorke/bdsim) models for the textbook "_Robotics, Vision & Control, edition 3 in Python_".

[bdsim](https://github.com/petercorke/bdsim) is a Python package that allows you to express block diagrams in terms of lines of code, ie. create blocks and wires, and them simulate the time response of the system.

## The files

For each bdsim model called `model` there can be many related files

| File name      |     Description                  |
| -------------- | -------------------------------- |
| model.py       | a Python+bdsim implementation of the model |
| model.bd       | a block diagram drawn with bdedit (a JSON file) |
| model-main.py  | a "main" function called by a complex bdsim model file |


You can run a Python+bdsim model from the command line

```
% ./model.py
or
% python model.py
```

You can open a model file using bdedit

```
% bdedit model.bd
```

and execute it by pushing the run button.

You can run a model file directly by

```
% bdrun model.bd
```
which will parse the model file, build a block diagram and execute it.

For a "complex" model file that contains a "Main" block you need to run the main file

```
% python model-main.py
```

## Installing bdsim

bdsim requires Python 3.8 or better.

```
pip install bdsim
```

To run some of these models you need to have two additional Robotics Toolbox installed.  It is not a dependency of `bdsim`.

```
pip install roboticstoolbox-python
pip install machinevisiontoolbox-python
```