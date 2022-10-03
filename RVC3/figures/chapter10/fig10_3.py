#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

lam = np.linspace(300, 1000, 100)

sun_ground = loadspectrum(lam * nm, 'solar')
sun_blackbody = blackbody(lam * nm, 5778)
scale = 0.58e-4

eye_response = rluminos(lam * nm)

fig, ax1 = plt.subplots()  # create a figure and an axes

# set left axes
color1 = 'tab:blue'
l1 = ax1.plot(lam, sun_ground, '--', color=color1, label='sun at ground level')
l2 = ax1.plot(lam, sun_blackbody * scale, '-', color=color1, label='sun blackbody')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylabel(r'$E(\lambda)\,\, (W sr^{-1} m^{-2} mm^{-1}) \times$', color=color1)
ax1.set_xlabel('Wavelength (nm)')
plt.ylim(0, 1.6e9)

# set right axes
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color2 = 'tab:red'
l3 = ax2.plot(lam, eye_response, '-r', color=color2, label='human perceived brightness')
ax2.tick_params(axis='y', labelcolor=color2)

ax1.grid()
legend_lines = l1 + l2 + l3
legend_labels = [leg.get_label() for leg in legend_lines]
ax1.legend(legend_lines, legend_labels)
plt.xlim(300, 1000)
plt.ylim(0, 1)

# https://stackoverflow.com/questions/7906365/matplotlib-savefig-plots-different-from-show

rvcprint.rvcprint(subfig='a')


# Figure 10.3b

# In[72]:

plt.figure()
lam_water = np.linspace(400,700,30) 
water_spectrum = loadspectrum(lam_water * nm, 'water')
d = 5.0
T = 10.0**(- water_spectrum * d)

plt.plot(lam_water, T)
plt.grid()
plt.xlabel('Wavelength (nm)')
plt.ylabel(r'T($\lambda$)')
plt.xlim(400, 700)
plt.ylim(0, 1)
# plt.show(block=True)

rvcprint.rvcprint(subfig='b')
