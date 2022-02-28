#!/usr/bin/env python3

import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath import *
import matplotlib.pyplot as plt
import numpy as np

robot = ERobot2([
      ELink2(ET2.R(), name='link1'),
      ELink2(ET2.tx(1) * ET2.tx(1.2) * ET2.ty(-0.5) * ET2.R(), 
             name='link2', parent='link1'),
      ELink2(ET2.tx(1), name='ee_1', parent='link2'),
      ELink2(ET2.tx(1) * ET2.tx(0.6) * ET2.ty(0.5) * ET2.R(), 
             name='link3', parent='link1'),
      ELink2(ET2.tx(1), name='ee_2', parent='link3')
    ], name="branched")
robot.teach(np.radians([30, -50, 75]), block=False)

rvcprint.rvcprint(thicken=None)

