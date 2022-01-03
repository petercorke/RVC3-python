#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

lam = np.arange(350, 750) * nm
human = luminos(lam)

plt.figure()

plt.plot(lam / nm, human, color='tab:blue',label='human')
plt.ylabel('lm/W')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.ylim(0, 700)
plt.grid()
rvcprint.rvcprint(subfig='b')

cones = loadspectrum(lam, 'cones')
plt.figure()
plt.plot(lam / nm, cones[:, 0], 'r')
plt.plot(lam / nm, cones[:, 1], 'g')
plt.plot(lam / nm, cones[:, 2], 'b')
plt.ylabel('cone response')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.ylim(0, 1)
plt.grid()
plt.legend(['red (L) cone', 'green (M) cone', 'blue (S) cone'])

rvcprint.rvcprint(subfig='a')

# TODO ensure common x-axis ticks


# human = luminos(lambda)
# plot(lambda*1e9,  human)
# luminos(450e-9) / luminos(550e-9)
# clf
# plot(lambda*1e9,  human)

# ylabel('lm/W')
# xlabel('Wavelength (nm)')
# rvcprint('subfig', 'a', 'thicken', 1.5)

# clf
# cones = loadspectrum(lambda, 'cones.dat')
# plot(lambda*1e9, cones)
# plot(lambda*1e9, cones(:,1), 'r')
# hold on
# plot(lambda*1e9, cones(:,2), 'g')
# plot(lambda*1e9, cones(:,3), 'b')
# grid on

# xlabel('Wavelength nm)')
# ylabel('Cone response')
# h = legend('red (L) cone', 'green (M) cone', 'blue (S) cone')
# h.FontSize = 12
# rvcprint('subfig', 'b', 'thicken', 1.5)

