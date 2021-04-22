import rvcprint
from math import pi
from roboticstoolbox import *
from spatialmath import *
import matplotlib.pyplot as plt
import numpy as np

robot = ERobot2([
      ELink2(ETS2.r(), name='link1'),
      ELink2(ETS2.tx(1) * ETS2.tx(1.2) * ETS2.ty(-0.5) * ETS2.r(), 
             name='link2', parent='link1'),
      ELink2(ETS2.tx(1), name='ee_1', parent='link2'),
      ELink2(ETS2.tx(1) * ETS2.tx(0.6) * ETS2.ty(0.5) * ETS2.r(), 
             name='link3', parent='link1'),
      ELink2(ETS2.tx(1), name='ee_2', parent='link3')
    ])
robot.teach(np.radians([30, -50, 75]), block=False)

rvcprint.rvcprint(thicken=None)

