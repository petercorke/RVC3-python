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

# load .enpeda dataset, 12bit pixel values
args = dict(mono=True, dtype='uint8', maxintval=4095, roi=[20, 750, 20, 480])
lefts = ZipArchive('bridge-l.zip', filter='*.pgm', **args)
rights = ZipArchive('bridge-r.zip', filter='*.pgm', **args)

# camera intrinsics
f   =  985.939 # [pixel] focal length
u0  =  390.255 # [pixel] X-coordinate of principle
v0  =  242.329 # [pixel] Y-coordinate of principle
b   =  0.20    # [m] width of baseline of stereo camera rig

cam = CentralCamera(f=f, pp=[u0, v0], rho=[1, 1])
print(cam)

cv.setRNGSeed(0)

displacements = []
errors = []
nmatches = []

for left, right in zip(lefts, rights):
    print('-----------------', left.id)
    # plt.clf()
    # plt.imshow(image.A, cmap='gray')
    # smb.plot_text((20, 420), f"frame {image.id}", color='w', backgroundcolor='k', fontsize=12)

    # find corner features
    orbL = left.ORB(nfeatures=400, id='index')
    orbR = right.ORB(nfeatures=400)
    
    # robustly match left and right corner features
    # - stereo match
    matchLR = orbL.match(orbR)
    F = matchLR.estimate(cam.points2F, method='ransac')
    print(matchLR)

    matchLR = matchLR.inliers
    nmatches.append(len(matchLR))


    # F, resid, inliers = cam.points2F(LRmatch.p1, LRmatch.p2, method='ransac')



    # # keep the features and match objects for the inliers
    # k = Cs(1,mstereo.inlierx)  # index of inlier features
    # fl = fl(k)
    
    # mstereo = mstereo.inlier
    
    # triangulate 3D points
    # m2 = m[::100]  # short list of matches
    lines1 = cam.ray(matchLR.p1)
    T = SE3(b, 0, 0)
    lines2 = cam.move(T).ray(matchLR.p2)

    P, d = lines1.closest_to_line(lines2)
    print(np.nanmedian(d))

    # P is 3xN

    # p1 = p(1:2,:) p2 = p(3:4,:)

    # d = p1(1,:) - p2(1,:)
    # X = b * (p1(1,:) - u0) ./ d
    # Y = b * (p1(2,:) - v0) ./ d
    # Z = f * b ./ d
    # P = [X Y; Z]
    
    if left.id > 0:
        # if we have a previous frame
        
        # display two sequential stereo pairs
        plt.clf()
        view4 = Image.Tile([left, right, left_prev, right_prev], columns=2, sep=0)
        plt.imshow(view4.A, cmap='gray')
        
        matchLR.plot_correspondence('y', offset=(left.width, 0), linewidth=0.5)

        # temporal matching
        matchFB = orbL.match(orbL_prev)
        F = matchFB.estimate(cam.points2F, method='ransac')
        print(matchFB)

        matchFB = matchFB.inliers
        matchFB.plot_correspondence('y', offset=(0, left.height), linewidth=0.5)
        plt.pause(0.1)
        
        if left.id == 10:
            rvcprint.rvcprint(thicken=None)
        
        # now create a bundle adjustment problem
        
        ba = BundleAdjust(cam)
        
        c_left = ba.add_view(SE3(), fixed=True)  # first camera at origin (current frame)
        c_leftprev = ba.add_view(SE3())          # initial guess, zero motion (prev frame)

        for k, Pk in enumerate(P.T):  # for every 3D point from stereo
            if np.any(np.isnan(Pk)):
                continue  # discard bad matches

            id = matchLR[k].descriptor1.id
            m = matchFB.by_id1(id)
            if m is None:
                continue
            landmark = ba.add_landmark(Pk)
            ba.add_projection(c_left, landmark, m.p1)  # current left camera
            ba.add_projection(c_leftprev, landmark, m.p2)  # previous left camera

        # solve bundle adjustment, fix number of iterations
        X, error = ba.optimize(iterations=5)
        displacements.append(X[6:12])
        errors.append(error)

    # keep images and features for next cycle
    orbL_prev = orbL
    left_prev = left
    right_prev = right

    if left.id > 250:
        break

f = open('vo.pickle', 'wb')
d = dict(displacements=displacements, errors=errors, nmatches=nmatches)
pickle.dump(d, f)
f.close()
