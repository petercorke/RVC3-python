from roboticstoolbox import lspb
import matplotlib.pyplot as plt
import numpy as np

traj = lspb(0, 1, np.linspace(0, 1, 50))

np.max(traj.x)

# rvcprint('subfig', 'a', 'thicken', 1)

traj2 = lspb(0, 1, np.linspace(0, 1, 50), 1.2);
traj3 = lspb(0, 1, np.linspace(0, 1, 50), 2.0);

legends = ['nominal', '1.2', '2.0']
plotopts = {'markersize': 2}
textopts = {'fontsize': 12}

plt.subplot(311)
plt.plot(traj.x, np.c_[traj.y, traj2.y, traj3.y], '-o', **plotopts)
plt.legend(legends, loc='upper left')
plt.grid(True)
plt.ylabel('$y(t)$');
plt.xlim(0, max(traj.x))

plt.subplot(312)
plt.plot(traj.x, np.c_[traj.yd, traj2.yd, traj3.yd], '-o', **plotopts)
# plt.legend(legends, loc='upper left')
plt.grid(True)
plt.ylabel('$dy/dt$', **textopts)
plt.xlim(0, max(traj.x))

plt.subplot(313)
plt.plot(traj.x, np.c_[traj.ydd, traj2.ydd, traj3.ydd], '-o', **plotopts)
# plt.legend(legends, loc='upper left')
plt.grid(True)
plt.ylabel('$d^2 y/dt^2$', **textopts)
plt.xlim(0, max(traj.x))
plt.xlabel('t (seconds)', **textopts)

plt.show(block=True)

# plt.subplot(312)
# plot( [sd sd2 sd3]); grid;
# ylabel('$ds/dk$', 'FontSize', 16, 'Interpreter','latex');

# plt.subplot(313)
# plot([sdd sdd2 sdd3]); grid; 
# ylabel('$ds^2/dk^2$', 'FontSize', 16, 'Interpreter','latex');
# xlabel('k (step)');

# rvcprint('subfig', 'b', 'thicken', 1)