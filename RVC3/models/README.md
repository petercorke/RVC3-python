# bdsim models

This folder holds a number of [bdsim](https://github.com/petercorke/bdsim) models for the textbook "_Robotics, Vision & Control, edition 3 in Python_".

[bdsim](https://github.com/petercorke/bdsim) is a Python package that allows you to express block diagrams in terms of lines of code, ie. create blocks and wires, and them simulate the time response of the system.

## The models

|File  |  Chapter |      Description  |
| ---- | -------- | ----------------- |
| RRMC | 8        | resolved rate motion control, straight line |
| RRMC2 | 8       | resolved rate motion control, closed loop, circular motion |
| SEA  | 9       | series elastic actuator |
| vloop | 9      | velocity loop    |
| ploop | 9      | position loop    |


## Installing bdsim

```
pip install bdsim
```

To run these models you must also have the Robotics Toolbox installed.  It is not a dependency of `bdsim`.

```
pip install roboticstoolbox-python
```