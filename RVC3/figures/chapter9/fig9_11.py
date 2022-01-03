import matplotlib.pyplot as plt
import rvcprint

import bdsim

import fig9_7 as vloop_test

vloop_test.bd['disturbance'].set_param('value', 40/107.815)
out = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["demand[0]", "vloop/out[0]"])


plt.plot(out.t, out.y0, 'r', label='demand')
plt.plot(out.t, out.y1, 'b', label='actual')
plt.grid(True)
plt.xlim(0, 0.6)
plt.ylim(-5, 55)

plt.legend()
plt.ylabel(r'$\mathbf{\omega}\, (\mathrm{rad\, s^{-1}})$')
plt.xlabel('Time (s)')

rvcprint.rvcprint()