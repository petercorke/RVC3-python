#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9


# Figure 10.2(a)

lam = np.linspace(300, 1000, 50)
for T in [3000, 4000, 5000, 6000]:
    e = blackbody(lam * nm, T)
    plt.plot(lam, e, label=f"{T}K")
plt.grid(True)
plt.xlabel('Wavelength (nm)')
plt.ylabel('$E(\lambda)\,\, (W sr^{-1} m^{-2} m^{-1})$')
plt.legend()
plt.xlim(300, 1000)

rvcprint.rvcprint(subfig='a')

# Figure 10.2(b), need to add human eye response

plt.figure()
lam = np.linspace(300, 1000, 50)

e = blackbody(lam * nm, 2600)
plt.plot(lam, e / max(e), label="Tungsten lamp (2600K)")

e = blackbody(lam * nm, 5778)
plt.plot(lam, e / max(e), label="Sun (5778K)")

eye = rluminos(lam * nm)
plt.plot(lam, eye, linestyle='--', label='human perceived brightness')

plt.grid(True)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized $E(\lambda)$')
plt.legend()
plt.xlim(300, 1000)
plt.ylim(0, 1)

rvcprint.rvcprint(subfig='b')

# lambda = [300:10:1000]*1e-9
# for T=1000:1000:6000
# plot( lambda*1e9, blackbody(lambda, T)) hold all
# end
# xaxis[299,999]
# h = legend('3000K', '4000K', '5000K', '6000K')
# h.FontSize = 12
# xlabel('Wavelength (nm)')
# ylabel('E(\lambda) (W sr^{-1} m^{-2} m^{-1})')

# rvcprint('subfig', 'a', 'thicken', 1.5)

# clf
# lamp = blackbody(lambda, 2600)
# sun = blackbody(lambda, 5778)
# plot(lambda*1e9, [lamp/max(lamp) sun/max(sun)])
# hold on
# plot(lambda*1e9, rluminos(lambda), 'g--')
# xlabel('Wavelength (nm)')
# ylabel('Normalized E(\lambda)')
# xaxis[299,999]
# yaxis[-1,0]
# legend('Tungsten lamp (2600K)', 'Sun (5778K)', 'Human eye response', 'Location', 'southeast')
# rvcprint('subfig', 'b', 'thicken', 1.5)

# max(sun)/max(lamp)
