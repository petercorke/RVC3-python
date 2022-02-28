#!/usr/bin/env python3

from roboticstoolbox import models
from spatialmath import SE3
import time

panda = models.URDF.Panda();
from spatialgeometry import Cuboid
box = Cuboid([1, 1, 1], pose=SE3(1.1, 0, 0));
panda.collided(panda.qr, box)
panda.collided(panda.qr, box)
# plot robot and get reference to graphics environment
env = panda.plot(panda.qr, backend="swift")  
env.add(box)  # add box to graphics
env.step()  # update the graphics

time.sleep(2)
box.base = SE3.Tx(1)
env.step()
c = panda.collided(panda.qr, box)
print(c)

# for i in range(20):
#     box.base = SE3(1.1 - i * 0.01, 0, 0)
#     c = panda.collided(panda.qr, box)
#     print(i, c)
#     env.step()
#     time.sleep(0.5)
env.hold()