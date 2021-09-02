#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import *

panda = models.ETS.Panda()

panda.plot(panda.qr, backend='pyplot')

rvcprint.rvcprint(thicken=None)