

# # B Linear Algebra
#

# ## B.2 Matrices
#

# ### B.2.1 Square Matrices
#

%run -m eigdemo 1 2 3 4

# # C Geometry
#

# ## C.1 Euclidean Geometry
#

# ### C.1.2 Lines
#


# #### C.1.2.2 Lines in 3D and Plücker Coordinates
#

P = [2, 3, 4]; Q = [3, 5, 7];

L = Line3.Join(P, Q)

L.v.T
L.w.T

L.skew()

plotvol3([-5, 5]);
L.plot("b");

L.point([0, 1, 2])

[x, d] = L.closest_to_point([1, 2, 3])
x
d

p, _ = L.intersect_plane([0, 0, 1, 0])
p


# ### C.1.4 Ellipses and Ellipsoids
#

E = np.array([[1, 1], [1, 2]])

plot_ellipse(E)

e, v = np.linalg.eig(E)
e
v

r = 1 / np.sqrt(e)

plot_arrow((0, 0), v[:,0]*r[0], color="r", width=0.02);
plot_arrow((0, 0), v[:,1]*r[1], color="b", width=0.02);

np.rad2deg(np.arctan2(v[1, 0], v[0, 0]))

# ### C.1.4.1 Drawing an Ellipse
#

E = np.array([[1, 1], [1, 2]]);

th = np.linspace(0, 2*pi, 50);
y = np.vstack([np.cos(th), np.sin(th)]);

x = sp.linalg.sqrtm(sp.linalg.inv(E)) @ y;
plt.plot(x[0, :], x[1, :], '.');

plot_ellipse(E, [0, 0])

# #### C.1.4.2 Fitting an Ellipse to Data
#

rng = np.random.default_rng(0);
# create 200 random points inside the ellipse
x = [];
while len(x) < 200: 
  p = rng.uniform(low=-2, high=2, size=(2,1))
  if np.linalg.norm(p.T @ E @ p) <= 1:
    x.append(p)
x = np.hstack(x);  # create 2 x 50 array
plt.plot(x[0, :], x[1, :], "k."); # plot them
# compute the moments
m00 = mpq_point(x, 0, 0);
m10 = mpq_point(x, 1, 0);
m01 = mpq_point(x, 0, 1);
xc = np.c_[m10, m01] / m00;
# compute the central second moments
x0 = x - xc.T;
u20 = mpq_point(x0, 2, 0);
u02 = mpq_point(x0, 0, 2);
u11 = mpq_point(x0, 1, 1);
# compute inertia tensor and ellipse matrix
J = np.array([[u20, u11], [u11, u02]]);
E_est = m00 / 4 * np.linalg.inv(J);

E_est

plot_ellipse(E_est, "r")

# ## C.2 Homogeneous Coordinates
#

# ### C.2.1 Two Dimensions
#

# #### C.2.1.1 Points and lines
#

l1 = [1, -1, 0];
l2 = [1, -1, -1];

plot_homline(l1, "b");
plot_homline(l2, "r");

np.cross(l1, l2)

# # E Linearizations, Jacobians and Hessians

# ## E.4 Deriving Jacobians
#

zrange = lambda xi, xv, w: np.array([
           np.linalg.norm(xi - xv[:2]) + w[0],
           np.arctan((xi[1] - xv[1]) / (xi[0] - xv[0])) -xv[2] + w[1]]);

xv = np.r_[1, 2, pi/3]; xi = np.r_[10, 8]; w = np.r_[0, 0];
h0 = zrange(xi, xv, w)
d = 0.001;
J = np.column_stack([
       zrange(xi, xv + [d, 0, 0], w) - h0,
       zrange(xi, xv + [0, d, 0], w) - h0,
       zrange(xi, xv + [0, 0, d], w) - h0
                    ]) / d

numjac(lambda x: zrange(xi, x, w), xv)

from sympy import Matrix, MatrixSymbol, sqrt, atan, simplify, pycode
xi = MatrixSymbol("xi", 2, 1)
xv = MatrixSymbol("xv", 3, 1)
w = Matrix([0, 0])

zrange = lambda xi, xv, w: Matrix([
            sqrt((xi[0] - xv[0])**2 + (xi[1] - xv[1])**2) + w[0],
            atan((xi[1] - xv[1]) / (xi[0] - xv[0])) -xv[2] + w[1]]);
z = zrange(xi, xv, w)

J = z.jacobian(xv)

J.shape

# # F Solving Systems of Equations
#

# ## F.1 Linear Problems
#

# ### F.1.1 Nonhomogeneous Systems
#

x = sp.linalg.spsolve(A, b)

# ### F.1.2 Homogeneous Systems
#

# ### F.1.3 Finding a Rotation Matrix
#


# flesh this out


# # G Gaussian Random Variables

x = np.linspace(-6, 6, 500);
plt.plot(x, gauss1d(0, 1, x), "r");
plt.plot(x, gauss1d(0, 2**2, x), "b--");

g = np.random.normal(loc=mu, scale=sigma, size=(100,));

x, y = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100));
P = np.diag([1, 2])**2;
g = gauss2d([0, 0], P, x, y);
ax = ax = plotvol3();
ax.plot_surface(x, y, g);
ax.contour(x, y, g, zdir="z", offset=-0.05);

from scipy.stats.distributions import chi2
chi2.ppf(0.5, 2)

# # H Kalman Filter
#

# ## H.2 Nonlinear Systems -- Extended Kalman Filter
#

x = np.random.normal(5, 2, size=(1_000_000,));

y = (x + 2)**2 / 4;

plt.hist(y, bins=200, density=True, histtype="step");


# # I Graphs
#

import pgraph
g = pgraph.UGraph()

np.random.seed(0)  # ensure repeatable results
for i in range(5):
  g.add_vertex(np.random.rand(2));

g[1]

g["#1"]

g.add_edge(g[0], g[1]);
g.add_edge(g[0], g[2]);
g.add_edge(g[0], g[3]);
g.add_edge(g[1], g[2]);
g.add_edge(g[1], g[3]);
g.add_edge(g[3], g[4]);

print(g)

g.plot()

g[1].adjacent()

g[1].edges()

g[1].edges()[0].endpoints

g[1].edges()[0].cost

g.closest((0.5, 0.5))

path, length, _ = g.path_Astar(g[2], g[4])
path

length

# # J Peak Finding
#

# ## J.1 1D Signal
#

y = mvtb_load_matfile("data/peakfit.mat")["y"];
plt.plot(y, "-o");

k = np.argmax(y)

y[k]

k, ypk = findpeaks(y)
k
ypk

ypk[1] / ypk[0]

findpeaks(y, interp=True)

findpeaks(y, scale=5)

# ## J.2 2D Signal
#

img = mvtb_load_matfile("data/peakfit.mat")["image"]

k = np.argmax(img)

img.ravel()[k]

np.unravel_index(k, img.shape)

xy = findpeaks2d(img)

xy = findpeaks2d(img, interp=True)

