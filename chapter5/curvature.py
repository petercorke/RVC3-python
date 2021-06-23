
import math
import scipy.integrate
import scipy.optimize
import numpy as np
import matplotlib.pyplot as plt


def solvepath(poly, s_f, x0=[0, 0, 0], **kwargs):

    def dotfunc(t, x, poly):
        theta = x[2]
        k = poly[0] * t ** 3 + poly[1] * t ** 2 + poly[2] * t + poly[3]
        return math.cos(theta), math.sin(theta), k

    sol = scipy.integrate.solve_ivp(dotfunc, [0, s_f], x0, args=(poly,), **kwargs)
    return sol.y

def costfunc(unknowns, goal):
    # p[0:4] is polynomial
    # p[4] is s_f
    path = solvepath(poly=unknowns[:4], s_f=unknowns[4])
    return np.linalg.norm(path[:, -1] - np.r_[goal])

sol = scipy.optimize.minimize(costfunc, [0, 0, 0, 1, 2], args=([1, 2, math.pi/4],))
print(sol.x)

path = solvepath(sol.x[:4], sol.x[4], dense_output=True, max_step = 1e-2)
plt.plot(path[0,:], path[1, :])
plt.show(block=True)