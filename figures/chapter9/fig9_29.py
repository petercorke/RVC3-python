#!/usr/bin/env python3

from rvcprint import rvcprint
import matplotlib.pyplot as plt
import site
# site.addsitedir('bdsim')
site.addsitedir('models')

from models.SEA import SEA

out = SEA(obstacle_pos=2)
print(out)
print(out.xnames)

t = out.t
u = out.y0
Fs = out.y1
x2 = out.x[:,3]

plt.figure()
plt.plot(t, x2)
plt.plot(t, u, '--')
plt.plot(t, Fs)

plt.ylim(-2, 2.5)
plt.grid(True)
plt.legend(['$x_2$', '$u$', '$F_s$'])
plt.xlabel('Time (s)')
plt.pause(2)

rvcprint(subfig='a')

# ----------------------------------------------------------------------- #

out = SEA(obstacle_pos=0.8)

t = out.t
u = out.y0
Fs = out.y1
x2 = out.x[:,3]

plt.figure()
plt.plot(t, x2)
plt.plot(t, u, '--')
plt.plot(t, Fs)

plt.ylim(-2, 2.5)
plt.grid(True)
plt.legend(['$x_2$', '$u$', '$F_s$'])
plt.xlabel('Time (s)')
plt.pause(2)

rvcprint(subfig='b')