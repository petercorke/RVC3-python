from roboticstoolbox import *
from spatialmath import base
import sympy

a1, a2 = sympy.symbols('a1 a2')
e = ETS2.r() * ETS2.tx(a1) * ETS2.r() * ETS2.tx(a2);

q0, q1 = sympy.symbols('q0 q1')
TE = e.eval([q0, q1])
print(TE)

xfk = TE.t[0]; yfk = TE.t[1];

x, y = sympy.symbols('x y')

eq1 = (xfk**2 + yfk**2 - x**2 - y**2).trigsimp()  

q1_sol = sympy.solve(eq1, q1)
print(q1_sol)

eq0 = *map(sympy.expand_trig, [xfk - x, yfk - y]),
q0_sol = sympy.solve(eq0, [sympy.sin(q0), sympy.cos(q0)])
q0 = sympy.atan(q0_sol[sin(q0)] / q0_sol[cos(q0)]).simplify()
pprint(q0)

# ---------

import scipy as sp
import numpy as np

e = ETS2.r() * ETS2.tx(1) * ETS2.r() * ETS2.tx(1)

pstar = np.r_[0.6, 0.7]
sol = sp.optimize.minimize(lambda q: np.linalg.norm(e.eval(q).t - pstar ), [0, 0])

print(sol.x)
e.eval(sol.x).printline()