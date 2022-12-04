import rvcprint
import numpy as np
from scipy.cluster.vq import kmeans2
import matplotlib.pyplot as plt
from spatialmath.base import plot_point

np.random.seed(0)

a = np.random.rand(500, 2)  # 500 x 2D data points

centres, labels = kmeans2(data=a, k=3)
print(centres.shape, labels.shape)

colors = ['red', 'green', 'blue']
for i in range(3):
    plot_point(a[labels==i, :].T, color=colors[i], marker='.', markersize=10)
    plot_point(centres[i, :].T, color=colors[i], marker='o', alpha=0.5, markeredgecolor='none', markersize=20)    

plt.gca().set_aspect(1)
plt.grid(True)
rvcprint.rvcprint(thicken=False)
# // r

# // clf
# // %fmt = {'r.', 'g.', 'b.'}; 
# // hold on
# // for i=1:3 plot( a(1,cls==i), a(2,cls==i), '.', 'MarkerSize', 10 ); end
# // % plot_point(a(:,cls==1), 'r.', 'MarkerSize', 10);
# // % plot_point(a(:,cls==2), 'g.', 'MarkerSize', 10);
# // % plot_point(a(:,cls==3), 'b.', 'MarkerSize', 10);

# // plot_point(centre, 'ok', 'MarkerFaceColor', 'k', 'MarkerSize', 12)
# // axis equal
# // xaxis(0,1); yaxis(0,1)
# // rvcprint