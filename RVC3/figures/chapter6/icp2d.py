from scipy.spatial import KDTree
import numpy as np

# reference or target 2xN
# source  2xN

# params:
#   source_points: numpy array containing points to align to the reference set
#                  points should be homogeneous, with one point per row
#   reference_points: numpy array containing points to which the source points
#                  are to be aligned, points should be homogeneous with one
#                  point per row
#   initial_T:     initial estimate of the transform between reference and source
# def __init__(self, source_points, reference_points, initial_T):
# 	self.source = source_points
# 	self.reference = reference_points
# 	self.init_T = initial_T
# 	self.reference_tree = KDTree(reference_points[:,:2])
# 	self.transform = self.AlignICP(30, 1.0e-4)

# uses the iterative closest point algorithm to find the
# transformation between the source and reference point clouds
# that minimizes the sum of squared errors between nearest 
# neighbors in the two point clouds
# params:
#   max_iter: int, max number of iterations
#   min_delta_err: float, minimum change in alignment error
def ICP2d(reference, source, T=None, max_iter=20, min_delta_err=1e-4):

    mean_sq_error = 1.0e6 # initialize error as large number
    delta_err = 1.0e6    # change in error (used in stopping condition)
    num_iter = 0         # number of iterations
    if T is None:
        T = np.eye(3)

    ref_kdtree = KDTree(reference.T)
    tf_source = source

    source_hom = np.vstack((source, np.ones(source.shape[1])))

    while delta_err > min_delta_err and num_iter < max_iter:

        # find correspondences via nearest-neighbor search
        matched_ref_pts, matched_source, indices = FindCorrespondences(ref_kdtree, tf_source, reference)

        # find alingment between source and corresponding reference points via SVD
        # note: svd step doesn't use homogeneous points
        new_T = AlignSVD(matched_source, matched_ref_pts)

        # update transformation between point sets
        T = T @ new_T

        # apply transformation to the source points
        tf_source = T @ source_hom
        tf_source = tf_source[:2, :]

        # find mean squared error between transformed source points and reference points
        # TODO: do this with fancy indexing
        new_err = 0
        for i in range(len(indices)):
            if indices[i] != -1:
                diff = tf_source[:, i] - reference[:, indices[i]]
                new_err += np.dot(diff,diff.T)

        new_err /= float(len(matched_ref_pts))

        # update error and calculate delta error
        delta_err = abs(mean_sq_error - new_err)
        mean_sq_error = new_err
        print('ITER', num_iter, delta_err, mean_sq_error)

        num_iter += 1

    return T


def FindCorrespondences(tree, source, reference):

    # get distances to nearest neighbors and indices of nearest neighbors
    dist, indices = tree.query(source.T)

    # remove multiple associatons from index list
    # only retain closest associations
    unique = False
    matched_src = source.copy()
    while not unique:
        unique = True
        for i, idxi in enumerate(indices):
            if idxi == -1:
                continue
            # could do this with np.nonzero
            for j in range(i+1,len(indices)):
                if idxi == indices[j]:
                    if dist[i] < dist[j]:
                        indices[j] = -1
                    else:
                        indices[i] = -1
                        break
    # build array of nearest neighbor reference points
    # and remove unmatched source points
    point_list = []
    src_idx = 0
    for idx in indices:
        if idx != -1:
            point_list.append(reference[:,idx])
            src_idx += 1
        else:
            matched_src = np.delete(matched_src, src_idx, axis=1)

    matched_ref = np.array(point_list).T

    return matched_ref, matched_src, indices

# uses singular value decomposition to find the 
# transformation from the reference to the source point cloud
# assumes source and reference point clounds are ordered such that 
# corresponding points are at the same indices in each array
#
# params:
#   source: numpy array representing source pointcloud
#   reference: numpy array representing reference pointcloud
# returns:
#   T: transformation between the two point clouds
def AlignSVD(source, reference):

    # first find the centroids of both point clouds
    src_centroid = source.mean(axis=1)
    ref_centroid = reference.mean(axis=1)

    # get the point clouds in reference to their centroids
    source_centered = source - src_centroid[:, np.newaxis]
    reference_centered = reference - ref_centroid[:, np.newaxis]

    # compute the moment matrix
    M = reference_centered @ source_centered.T

    # do the singular value decomposition
    U, W, V_t = np.linalg.svd(M)

    # get rotation between the two point clouds
    R = U @ V_t
    if np.linalg.det(R) < 0:
        raise RuntimeError('bad rotation matrix')

    # translation is the difference between the point clound centroids
    t = ref_centroid - R @ src_centroid

    return rt2tr(R, t)


def closest(P, Q):
    D = np.full((P.shape[1], Q.shape[1]), np.inf)
    for i in range(P.shape[1]):
        Pi = P[:, i]
        Di = Q - Pi[:, np.newaxis]
        di = np.linalg.norm(Di, axis=0)
        D[i, :] = di

    return D

import pickle
from spatialmath.base import *
import matplotlib.pyplot as plt

data = pickle.load(open('scans.p', 'rb'))

s1 = data['s1']
s2 = data['s2']


s1 = s1[:, ~np.isnan(s1[0,:])]
s2 = s2[:, ~np.isnan(s2[0,:])]

# D = closest(s1, s2)

print(s1.mean() - s2.mean())


T = ICP2d(s1, s2, transl2(0, 0))
print(T)