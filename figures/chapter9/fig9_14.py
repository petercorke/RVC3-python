#!/usr/bin/env python3

import matplotlib.pyplot as plt
import rvcprint
import site

site.addsitedir('../../models')

import ploop_test

# import cProfile, pstats
# profiler = cProfile.Profile()
# profiler.enable()
# out = ploop_test.sim.run(ploop_test.bd, 1, dt=1e-3, watch=["PLOOP/out[0]", "quintic[0]"])
# profiler.disable()
# stats = pstats.Stats(profiler).sort_stats('cumtime')
# stats.dump_stats('bdsim.profile')

ploop_test.sim.set_options(hold=False)

out = ploop_test.sim.run(ploop_test.bd, 1, dt=1e-3, watch=["PLOOP/out[0]", "quintic[0]"])

plt.figure()
plt.plot(out.t, out.y1, 'r', label='demand')
plt.plot(out.t, out.y0, 'b', label='actual')
plt.grid(True)
plt.xlim(0, 1)
plt.ylim(-0.1, 1.1)
plt.legend()
plt.ylabel('q (rad)')
rvcprint.rvcprint(subfig='a')

# ------------------------------------------------------------------------- #

ploop_test.bd['PLOOP/Kff'].set_param('K', 107.0)
out = ploop_test.sim.run(ploop_test.bd, 1, dt=1e-3, watch=["PLOOP/out[0]", "quintic[0]"])

plt.figure()
plt.plot(out.t, out.y1, 'r', label='demand')
plt.plot(out.t, out.y0, 'b', label='actual')
plt.grid(True)
plt.xlim(0, 1)
plt.ylim(-0.1, 1.1)
plt.legend()
plt.ylabel('q (rad)')
rvcprint.rvcprint(subfig='b')

# import matplotlib.pyplot as plt
# plt.show(block=True)