#! /usr/bin/env python3

from roboticstoolbox import trapezoidal
import matplotlib.pyplot as plt
import numpy as np
from rvcprint import rvcprint
from cycler import cycler

traj = trapezoidal(0, 1, np.linspace(0, 1, 50))
traj.plot()
plt.gcf().get_axes()[0].legend()

rvcprint(subfig='a', thicken=1)

traj2 = trapezoidal(0, 1, np.linspace(0, 1, 50), 1.2);
traj3 = trapezoidal(0, 1, np.linspace(0, 1, 50), 2.0);

legends = ['nominal', '1.2', '2.0']
plotopts = {'markersize': 2}
textopts = {'fontsize': 12}

custom_cycler = cycler(color=['r', 'g', 'b'])

ax = plt.subplot(311)
ax.set_prop_cycle(custom_cycler)
lines = ax.plot(traj.t, np.c_[traj.q, traj2.q, traj3.q], '-o', **plotopts)
ax.legend(lines, legends, loc='upper left')
ax.grid(True)
ax.set_ylabel('$q(t)$');
ax.set_xlim(0, max(traj.t))

plt.subplot(312)
plt.gca().set_prop_cycle(custom_cycler)
plt.plot(traj.t, np.c_[traj.qd, traj2.qd, traj3.qd], '-o', **plotopts)
# plt.legend(legends, loc='upper left')
plt.grid(True)
plt.ylabel('$\dot{q}(t)$', **textopts)
plt.xlim(0, max(traj.t))

plt.subplot(313)
plt.gca().set_prop_cycle(custom_cycler)
plt.plot(traj.t, np.c_[traj.qdd, traj2.qdd, traj3.qdd], '-o', **plotopts)
# plt.legend(legends, loc='upper left')
plt.grid(True)
plt.ylabel('$\ddot{q}(t)$', **textopts)
plt.xlim(0, max(traj.t))
plt.xlabel('t (seconds)', **textopts)


# plt.subplot(312)
# plot( [sd sd2 sd3]); grid;
# ylabel('$ds/dk$', 'FontSize', 16, 'Interpreter','latex');

# plt.subplot(313)
# plot([sdd sdd2 sdd3]); grid; 
# ylabel('$ds^2/dk^2$', 'FontSize', 16, 'Interpreter','latex');
# xlabel('k (step)');

rvcprint(subfig='b', thicken=1)