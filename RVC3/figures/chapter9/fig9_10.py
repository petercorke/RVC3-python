#!/usr/bin/env python3

import matplotlib.pyplot as plt
import rvcprint

import bdsim

import vloop_test
vloop_test.sim.set_options(hold=False)

vloop_test.bd['VLOOP/motor'].set_param('den', [200e-6, vloop_test.B])
out_0 = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["VLOOP/out[0]"])

vloop_test.bd['VLOOP/motor'].set_param('den', [515e-6, vloop_test.B])
out_1 = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["VLOOP/out[0]"])

vloop_test.bd['VLOOP/motor'].set_param('den', [580e-6, vloop_test.B])
out_2 = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["VLOOP/out[0]"])

vloop_test.bd['VLOOP/motor'].set_param('den', [648e-6, vloop_test.B])
out_3 = vloop_test.sim.run(vloop_test.bd, 1, dt=1e-3, watch=["VLOOP/out[0]"])

plt.plot(out_0.t, out_0.y0, label='no link inertia')
plt.plot(out_1.t, out_1.y0, label='min link inertia')
plt.plot(out_2.t, out_2.y0, label='mean link inertia')
plt.plot(out_3.t, out_3.y0, label='max link inertia')

plt.grid(True)
plt.xlim(0.29, 0.32)
plt.ylim(47, 51)
plt.legend()
plt.ylabel(r'$\mathbf{\omega}\, (\mathrm{rad\, s^{-1}})$')
plt.xlabel('Time (s)')

rvcprint.rvcprint()