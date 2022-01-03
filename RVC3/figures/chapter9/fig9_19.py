from rvcprint import rvcprint
import matplotlib.pyplot as plt
from roboticstoolbox import xplot

import fig9_18 as zt

out = zt.sim.run(zt.bd, 5)  # simulate for 5s

plt.figure()
xplot(out.t, out.x[:,:3])
plt.ylabel('q (rad)')
plt.grid(True)
plt.xlabel('Time (s)')
rvcprint()