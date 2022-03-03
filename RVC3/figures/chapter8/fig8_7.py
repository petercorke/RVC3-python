#! /usr/bin/env python3
import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath.base import *
import matplotlib.pyplot as plt
import numpy as np

a1 = 1
a2 = 1

robot = ERobot2(ET2.R() * ET2.tx(a1) * ET2.R() * ET2.tx(a2))

# robot.teach([0,0], block=True, vellipse=True)
robot.teach(np.radians([30, 40]), vellipse=True, block=False)

rvcprint.rvcprint(thicken=None)