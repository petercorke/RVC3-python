import rvcprint
from roboticstoolbox import *

a1 = 1
e = ETS2.r() * ETS2.tx(a1);

r = ERobot2(e)
r.teach(40, unit='deg', block=False)

rvcprint.rvcprint()