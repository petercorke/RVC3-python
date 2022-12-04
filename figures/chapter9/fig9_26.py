#!/usr/bin/env python3

from rvcprint import rvcprint
import matplotlib.pyplot as plt
from cycler import cycler
import site
# site.addsitedir('bdsim')
site.addsitedir('models')

from models.opspace import sim, bd, robot_x, ftsensor

sim.set_options(graphics = False, hold=False)

out = sim.run(bd, 2, dt=5e-3, watch=[robot_x.x, ftsensor])
sim.done(bd, block=True)
print(out.xnames)

t = out.t
x = out.y0
ft = out.y1
print(out)

plt.figure()
f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
a0.set_prop_cycle(cycler(color=['red', 'green', 'blue']))
a0.plot(t, x[:, :3])
a0.axhline(y=0.5, color='b', linestyle='--')
a0.grid(True)
a0.legend(['x', 'y', 'z', '$z_t$'])
a0.set_ylabel('EE position (m)')
a0.set_xlim(0, 2)
a0.set_xticklabels([])

a1.plot(t, ft[:, 2], 'k')
a1.grid(True)
a1.set_ylabel('$F_z$ (N)')
a1.set_xlabel('Time (s)')
a1.set_xlim(0, 2)

rvcprint()
