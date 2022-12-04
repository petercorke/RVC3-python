from math import inf
import numpy as np
from spatialmath import SE2

def gpc(X, Y, C=None):
	
    if C is None:
        C = np.eye(2)
    
    ## First we put the problem in a quadratic+constraint form.
    M = np.zeros((4,4))
    g = np.zeros((4,))

    # rot(pi/2)
    R = np.array([[0.0, -1.0], [1.0, 0.0]])

    for x, y in zip(X.T, Y.T):
        M_k = np.block([np.eye(2), np.c_[x, R @ x]])
        M += M_k.T @ C @ M_k
        g += (- 2 * y @ C @ M_k).T

    W = np.block([
            [np.zeros((2,2)), np.zeros((2,2))],
            [np.zeros((2,2)), np.eye(2)]
            ])

    ## Partition M into 4 submatrixes: [A B; C D]
    M = 2 * M
    A = M[:2, :2]
    B = M[:2, 2:]
    D = M[2:, 2:]
    invA = np.linalg.inv(A)

    S = D - B.T @ invA @ B
    Sa = np.linalg.inv(S) * np.linalg.det(S)
    
    # create column vectors
    g1 = g[:2].reshape((2,1))
    g2 = g[2:].reshape((2,1))

    # polynomials are arrays with highest-order coefficient first
    p7 = [
        g1.T@(invA @ B @   (4       * B.T) @ invA) @ g1 + 2 * g1.T @ (-invA @ (B *   4)  )   @ g2  + g2.T @ ( 4      * g2),
        g1.T@(invA @ B @   (4 * Sa)  @ B.T @ invA) @ g1 + 2 * g1.T @ (-invA @ B @   (4 * Sa)) @ g2  + g2.T @ ( 4 * Sa) @ g2,
        g1.T@(invA @ B @  Sa @ Sa  @ B.T @ invA) @ g1 + 2 * g1.T @ (-invA @ B @  Sa @ Sa) @ g2  + g2.T @ (Sa @ Sa) @ g2
    ]
    # result is a list of 1x1 NumPy arrays, fix that
    p7 = np.array(p7).ravel()
            
    p_lambda = [
        4, 
        (2 * S[0, 0] + 2 * S[1, 1]), 
        (S[0, 0] * S[1, 1] - S[1, 0] * S[0, 1])
        ]
    Ptot = np.polyadd(p7, -np.polymul(p_lambda, p_lambda))

    # Find largest real root of Ptot
    roots = np.roots(Ptot)
    lam, found = 0, False
    for root in roots:
        if np.isreal(root) and (not found or root > 0):
            root = np.real(root)
            lam = max(lam, root);
            found = True

    x = -np.linalg.inv(M + 2 * lam * W) @ g
    theta = np.arctan2(x[3], x[2])

    return SE2(*x[:2], theta)

# def correspondence(yp, yt, T):
#     # Out of the main loop, we remember the last match found. int last_best = invalid;

#     # C++ code
#     from = 0
#     to = nrays
#     dtheta = (theta_max - theta_min) / nrays

#     for pi_w in scan yt: 
#         # Current best match, and its distance
#         best = invalid
#         best_dist = 1.0
        
#         # Approximated index in scan yp corresponding to point pi_w 

#         start_index =  int((theta_iw - theta_min) / dtheta)
        
#         # If last match was succesful, then start at that index + 1
#         if last_best == invalid:
#             we_start_at = start_index
#         else:
#             we_start_at = last_best + 1

#         # clip to the range [from, to]
#         we_start_at = min(to, max(we_start_at, from)

# 		if(we_start_at < from) we_start_at = from;

#         # Search is conducted in two directions: up and down
#         up = we_start_at + 1
#         down = we_start_at
        
#         # Distance of last point examined in the up (down) direction.
#         last_dist_up, last_dist_down = np.inf, np.inf
        
#         # True if search is ﬁnished in the up (down) direction.
#         up_stopped down_stopped = False, False

#         # Until the search is stopped in both directions...
#         while not (up_stopped and down_stopped):
#             # Should we try to explore up or down?

#             now_up = not up_stopped and (last_dist_up < last_dist_down)
        
#             # Now two symmetric chunks of code, the now_up and the !now_up

#             if now_up:
#                 # If we have ﬁnished the points to search, we stop
#                 if up >= nrays:
#                     up_stopped = True
#                     continue
                
#                 # just ignore invalid rays
#                 if not valid[up]:
#                     up += 1
#                     continue

#                 # This is the distance from p i w to the up point.
#                 last_dist_up = np.linalg.norm(pi_w - p_up)
                
#                 # If it is less than the best point, up is our best guess so far.
#                 if correspondence is acceptable and last_dist_up < best_dist:
#                     best = up
#                     best_dist = last_dist_up

#                 if up > start_index:
#                     # If we are moving away from start_cell we can compute a bound for early stopping. 
#                     # Currently our best point has distance best_dist; we can compute the minimum distance to p i w for points j > up (see ﬁgure 4(c)).

#                     delta_theta = theta_up - theta_iw
#                     min_dist_up = sin(delta_theta) * np.linalg.norm(pi_w)
#                     if min_dist_up ** 2 > best_dist:
#                         # If going up we can’t make better than best_dist,
#                         # then we stop searching in the "up" direction
#                         up_stopped = True
#                         continue
#                     # If we are moving away, then we can implement the jump tables optimization.

#                     # Next point to examine is...
#                     if rho_up < np.linalg.norm(pi_w):  # is p i w longer?

#                         up = up_bigger[u]  # then jump to a further point
#                     else:
#                         up = up_smaller[up] # else, to a closer one.

#                 else:
#                     # If we are moving towards "start_cell", we can’t do any ot the
#                     # previous optimizations and we just move to the next point. 
#                     up += 1
            
#             if not now_up:
#                 # This is the reflection of the previous chunk of code. 
#                 if down < from:
#                     down_stopped = True
#                     continue
#                 if 
#         # Set null correspondence if no point matched.

#         # For the next point, we will start at best 55 last_best = best; 56 }

def scanmatch(X, Y, T, ntheta=5):
    """

    :param X: first scan
    :type X: array_like(2,N)
    :param Y: second scan
    :type Y: array_like(2,N)
    :param T: estimate of transform from first scan to second 
    :type T: SE2
    :param ntheta: [description], defaults to 5
    :type ntheta: int, optional
    :return: [description]
    :rtype: [type]
    """
    # Censi paper
    # X y(t-1) p_j
    # Y y(t) p_i, p_i_w = T * p_i
    corr = []
    Yw = T * Y
    for j in range(X.shape[1]):
        jmin = max(0, j - ntheta)
        jmax = min(j + ntheta, X.shape[1])
        d2 = (Yw[:, jmin: jmax] - X[:, j].reshape((2,1))) ** 2
        try:
            k = np.nanargmin(d2.sum(axis=0))
            corr.append(k + jmin)
        except ValueError:
            # all NaN slice
            pass

    print(f"{len(corr)} corresponding points")
    return gpc(X[:, corr], Y[:, corr])

if __name__ == "__main__":

    import pickle

    data = pickle.load(open('scans.p', 'rb'))

    p = data['s1']
    q = data['s2']
    q = SE2(0.2, 0.3, 0.1) * p

    T = SE2()

    # noise = 0.0
    # theta = np.radians(4);
    # t = [0.3, -0.2]
    # real_x = [*t, theta];

    # p = np.array([[1, 0], [0, 1], [-1, 0], [2, 1], [4, 2]]).T
    # # alpha = [deg2rad(0);deg2rad(10);deg2rad(20);deg2rad(50);deg2rad(-20);];
    # T = SE2(real_x)
    # q = T * p + np.random.randn(*p.shape) * noise

    for i in range(10):
        T = scanmatch(p, q, T)

        # print(real_x)
        print(T)
