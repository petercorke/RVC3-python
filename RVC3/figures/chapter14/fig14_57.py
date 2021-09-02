#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm
import cv2 as cv
from spatialmath import SE3

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
lefts = ZipArchive('bridge-l.zip', grey=True, dtype='uint8', maxintval=4095, roi=[20, 750, 20, 480])
rights = ZipArchive('bridge-r.zip', grey=True, dtype='uint8', maxintval=4095, roi=[20, 750, 20, 480])

# camera intrinsics
f   =  985.939 # [pixel] focal length
u0  =  390.255 # [pixel] X-coordinate of principle
v0  =  242.329 # [pixel] Y-coordinate of principle
b   =  0.20    # [m] width of baseline of stereo camera rig

cam = CentralCamera(f=f, pp=[u0, v0], rho=[1, 1])

cv.setRNGSeed(0)

displacement = []

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

    matchLR = matchLR.inliers()


    # F, resid, inliers = cam.points2F(LRmatch.p1, LRmatch.p2, method='ransac')



    # # keep the features and match objects for the inliers
    # k = Cs(1,mstereo.inlierx)  # index of inlier features
    # fl = fl(k)
    
    # mstereo = mstereo.inlier
    
    # triangulate 3D points
    # m2 = m[::100]  # short list of matches
    lines1 = cam.plucker(matchLR.p1)
    T = SE3(b, 0, 0)
    lines2 = cam.move(T).plucker(matchLR.p2)

    P, _ = lines1.closest_to_line(lines2)

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

        matchFB = matchFB.inliers()
        matchFB.plot_correspondence('y', offset=(0, left.height), linewidth=0.5)
        plt.pause(0.1)
        
        # if camera.id == 10:
        #     rvcprint.rvcprint()
        #     break
        
        # now create a bundle adjustment problem
        
        ba = BundleAdjust(cam)
        
        c_left = ba.add_view(SE3(), fixed=True)  # first camera at origin (prev frame)
        c_leftprev = ba.add_view(SE3())

        for k, Pk in enumerate(P.T):
            if np.any(np.isnan(Pk)):
                continue

            id = matchLR[k].descriptor1.id
            m = matchFB.by_id1(id)
            if m is None:
                continue
            landmark = ba.add_landmark(Pk)
            ba.add_projection(c_left, landmark, matchLR[k].p1)  # current camera
            ba.add_projection(c_leftprev, landmark, m.p2)  # previous camera

        # solve bundle adjustment, fix number of iterations
        X = ba.optimize(iterations=5)
        displacement.append(X[6:12])

    # keep images and features for next cycle
    orbL_prev = orbL
    left_prev = left
    right_prev = right

    if left.id > 250:
        break

dd = np.array(displacement)
plt.figure()
plt.plot(dd[:,2])
plt.grid(True)
plt.xlabel('time')
plt.ylabel('z')

xy = np.cumsum(dd[:, :3], axis=0)
plt.figure()
plt.plot(xy[:,0], -xy[:,2])
plt.grid(True)
plt.xlabel('x')
plt.ylabel('z')

plt.figure()
plt.plot(xy[:,0])
plt.grid(True)
plt.xlabel('time')
plt.xlabel('x')


        # if image.id > 15:
        # break

# rvcprint.rvcprint
plt.show(block=True)
