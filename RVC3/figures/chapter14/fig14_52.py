#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv
from spatialmath import SE3
import pickle

## Visual odometry example
#   - stereo camera
#   - ICP between frames

# read images
#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import spatialmath.base as smb


print('loading pickled data')
f = open('vo.pickle', 'rb')
d = pickle.load(f)

displacements = d['displacements']
errors = d['errors']

disp = np.array(displacements)
disp_norm = np.linalg.norm(disp[:, :3], axis=1)

ts = np.loadtxt(mvtb_path_to_datafile('data/timestamps.dat'))
dt = np.r_[np.diff(ts), 0]

# some stats
print('maximum BA error', np.max(errors))
print('median BA error', np.median(errors))
print('median speed', np.median(disp_norm) / np.median(dt))

# plot histogram of BA errors
plt.hist(errors, bins=50, cumulative=True, density=True)
plt.grid(True)

# plot displacement
plt.figure(figsize=(8,4))
plt.subplot(3, 1, 1)
plt.plot(disp_norm, '.-', markersize=6, label='_nolegend_')
plt.ylim(0, 1.5)
plt.xlim(2, len(disp_norm))
plt.ylabel(r'$\mathbf{\|t\|}$ (m)')
plt.grid(True)

# overlay a cross on the bad timestamp values
k = np.nonzero(dt > 0.07)[0]
plt.plot(k, disp_norm[k], 'rx', markersize=6, label='missed video frame')
plt.legend(loc='lower left')

# plot BA error
plt.subplot(3, 1, 2)
plt.plot(np.r_[errors], '.-', markersize=6)
# plt.gca().set_yscale('log')
plt.xlim(2, len(errors))
# plot([2,length(tz)], [20 20], 'r--')
plt.ylabel('$\mathbf{e}$ (pix^2)')
plt.grid(True)

# plot time stamp deltas
plt.subplot(3, 1, 3)
plt.plot(dt, '.', markersize=4)
plt.ylim(0, 0.15)
plt.xlim(2, len(disp_norm))
plt.xlabel('Time step')
plt.ylabel('$\mathbf{\Delta T}$')
plt.grid(True)

rvcprint.rvcprint()






