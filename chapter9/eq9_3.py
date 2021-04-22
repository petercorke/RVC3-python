
from roboticstoolbox import *
from spatialmath.base import sym
from sympy import *

zero = sym.zero()
pi = sym.pi()
a1, a2 = sym.symbol('a1 a2')
m1, m2 = sym.symbol('m1 m2')
c1, c2 = sym.symbol('c1 c2')
g = sym.symbol('g')


links = [
        RevoluteDH(a=a1, alpha=zero, m=m1, r=[c1, 0, 0]),
        RevoluteDH(a=a2, alpha=zero, m=m2, r=[c2, 0, 0])
    ]

robot = DHRobot(links, symbolic=True)
print(robot)

q1, q1d, q1dd, q2, q2d, q2dd = sym.symbol('q1 q1d q1dd q2 q2d q2dd')
tau = robot.rne_python([q1, q2], [q1d, q2d], [q1dd, q2dd], gravity=[0, -g, 0])
print(tau[0])
print()
# t1 = tau[0].expand().simplify()

# t11 = t1.coeff(q1dd)
# M11 = collect(t11, (m1, m2))
# print('M11', M11)

# t12 = t1.coeff(q2dd)
# M12 = collect(t12, (m1, m2)).factor()
# print('M12', M12)

# C1 = t1.coeff(q1d).coeff(q2d).factor()
# print('C1', C1)
# C2 = t1.coeff(q2d, 2).factor()
# print('C2', C2)

# G = t1.coeff(g)
# G = collect(G, (cos(q1), cos(q1+q2)))
# print('G', G)

# --- now with ERobot

l0 = ELink(ETS.rz(), m=m1, r=[a1+c1, 0, 0])
l1 = ELink(ETS.tx(a1) * ETS.rz(), m=m2, r=[a2+c2, 0, 0], parent=l0)

robot = ERobot([l0, l1])

robot.fkine([0,0])

print(robot)
tau = robot.rne([q1, q2], [q1d, q2d], [q1dd, q2dd], gravity=[0, -g, 0], symbolic=True)
print(tau[0])
print()
t1 = tau[0].expand().simplify()

print()
t1 = tau[0].expand().simplify()

t11 = t1.coeff(q1dd)
M11 = collect(t11, (m1, m2))
print('M11', M11)

t12 = t1.coeff(q2dd)
M12 = collect(t12, (m1, m2)).factor()
print('M12', M12)

C1 = t1.coeff(q1d).coeff(q2d).factor()
print('C1', C1)
C2 = t1.coeff(q2d, 2).factor()
print('C2', C2)

G = t1.coeff(g)
G = collect(G, (cos(q1), cos(q1+q2)))
print('G', G)