#!/usr/bin/env python3

from rvcprint import rvcprint
import matplotlib.pyplot as plt
from roboticstoolbox import xplot

import zerotorque as zt
zt.sim.set_options(hold=False)

out = zt.sim.run(zt.bd, 5)  # simulate for 5s

plt.figure()
xplot(out.t, out.x[:,:3])
plt.ylabel('q (rad)')
plt.grid(True)
plt.xlabel('Time (s)')
rvcprint()