#!/usr/bin/env python3

import rvcprint
from roboticstoolbox import *

panda = models.ETS.Panda()

panda.plot(panda.qr, backend='pyplot')

print(panda)


# qt = jtraj(panda.qz, panda.qr, 100)
# panda.plot(qt.q, backend='pyplot')

rvcprint.rvcprint(thicken=None)