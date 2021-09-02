import numpy as np
import matplotlib.pyplot as plt
from spatialmath import base

W = np.diag([0.01, np.radians(1)]) ** 2
print(W)

z = np.random.multivariate_normal((0.1, 0.2), W, size=50000)

print(z)

C = np.cov(z.T)
print(C)

mu = np.mean(z, axis=0)
print(mu)

plt.plot(z[:,0], z[:,1], 'ok', markersize=2)
plt.grid(True)
base.plot_ellipse(C, confidence=0.99, centre=mu, inverted=True, color='g')
base.plot_ellipse(W, confidence=0.99, centre=mu, inverted=True, color='b')


plt.show(block=True)