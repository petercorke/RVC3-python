import matplotlib.pyplot as plt
import rvcprint

import bdsim

import fig9_7 as vloop_test

vloop_test.bd['disturbance'].set_param('value', 40/107.815)
vloop_test.bd['vloop/Ki'].set_param('K', 2.0)
out = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["demand[0]", "vloop/out[0]", "vloop/out[3]"])


plt.subplot(211)
plt.plot(out.t, out.y0, 'r', label='demand')
plt.plot(out.t, out.y1, 'b', label='actual')
plt.grid(True)
plt.xlim(0, 0.6)
plt.ylim(-5, 55)
plt.legend()
plt.ylabel(r'$\mathbf{\omega}\, (\mathrm{rad\,  s^{-1}})$')

plt.subplot(212)
plt.plot(out.t, out.y2, 'k')
plt.xlim(0, 0.6)
plt.ylim(0, 2)
plt.grid(True)
plt.xlabel('Time (s)')
plt.ylabel('Integral value')

rvcprint.rvcprint()

