# from roboticstoolbox import *
# from spatialmath import SE3
# from spatialgeometry import Box

# panda = models.URDF.Panda()
# box = Box([1, 1, 1], base=SE3(1, 0, 0))
# print(box)

# q = panda.qr
# hit = panda.collided(q, box)
# print(hit)

# d, p1, p2 = panda.closest_point(q, box)
# print(d, p1, p2)
# box.base.base = SE3(0.5, 0, 0)
# panda.collided(q, box)

# env = panda.plot(q, show_collision=True, backend='swift', block=True)

# # env = panda.plot(panda.qz, backend='swift')  # plot robot and get reference to graphics environment
# env.add(box)  # add box to graphics
# env.step()  # update the graphics


from roboticstoolbox import *
from spatialmath import SE3
from spatialgeometry import Box

panda = models.URDF.Panda()
box = Box([1, 1, 1], base=SE3(1, 0, 0), color='yellow')

env = panda.plot(panda.qr, show_collision=True, backend='swift')

# env = panda.plot(panda.qz, backend='swift')  # plot robot and get reference to graphics environment
env.add(box)  # add box to graphics
env.hold()  # update the graphics