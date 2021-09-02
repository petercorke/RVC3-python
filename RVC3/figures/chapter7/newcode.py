from roboticstoolbox import *

# [
#     ELink(ETS2.r(), name='link1'),
#     ELink(ETS2.tx(1) * ETS2.ty(-0.5) * ETS2.r(), name='link2', parent='link1'),
#     ELink(ETS2.tx(1), name='ee_1', parent='link2'),
#     ELink(ETS2.tx(1) * ETS2.ty(0.5) * ETS2.r(), name='link3', parent='link1'),
#     ELink(ETS2.tx(1), name='ee_2', parent='link3')
# ]


l1 = ELink(ETS2.r(), name='link1')
l2 = ELink(ETS2.tx(1) * ETS2.ty(-0.5) * ETS2.r(), name='link2', parent=l1)
ee1 = ELink(ETS2.tx(1), name='ee_1', parent=l2)
l3 = ELink(ETS2.tx(1) * ETS2.ty(0.5) * ETS2.r(), name='link3', parent=l1)
ee2 = ELink(ETS2.tx(1), name='ee_2', parent=l3)

robot = ERobot([l1, l2, ee1, l3, ee2])
print(robot)
robot.dotfile('2link.dot')


# this will be 