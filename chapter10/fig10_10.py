import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *

nm = 1e-9

lam = np.arange(350, 800, 5) * nm
cmf = cmfrgb(lam, method='cubic')

plt.plot(lam / nm, cmf[:,0], 'r', label='CIE red')
plt.plot(lam / nm, cmf[:,1], 'g', label='CIE green')
plt.plot(lam / nm, cmf[:,2], 'b', label='CIE blue')
plt.ylabel('color matching function')
plt.xlabel('Wavelength (nm)')
plt.xlim(350, 750)
plt.grid()
plt.legend()

rvcprint.rvcprint()

