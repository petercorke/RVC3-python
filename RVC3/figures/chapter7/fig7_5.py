#!/usr/bin/env python3

import rvcprint
import numpy as np
from roboticstoolbox import *

a1 = 1
e = ET2.R() * ET2.tx(a1);
r = ERobot2(e)
r.teach(np.deg2rad(40), block=False)

rvcprint.rvcprint()