import sympy
from spatialmath import SE2


xi, yi, ti, xj, yj, tj, xm, ym, tm = sympy.symbols('xi yi ti xj yj tj xm ym tm')

xi_e = SE2(xm, ym, tm).inv() * SE2(xi, yi, ti).inv() * SE2(xj, yj, tj)

fk = sympy.Matrix(sympy.simplify(xi_e.xyt()))

Ai = sympy.simplify(fk.jacobian([xi, yi, ti]))
print(Ai)
