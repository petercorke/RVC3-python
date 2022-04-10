#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

## Visual odometry example
#   - stereo camera
#   - ICP between frames

## read images
if ~exist('left')
left = iread('bridge-l/*.png', 'roi', [20 750 20 480])
right = iread('bridge-r/*.png', 'roi', [20 750 20 480])
end

# known camera parameters

# # ###############################################################################
# # # Camera parameter file                                                       #
# # ###############################################################################
# # 
# # [INTERNAL]
# # F        =  985.939 # [pixel] focal length
# # SX       =  1.0     # [pixel] pixel size in X direction
# # SY       =  1.0     # [pixel] pixel size in Y direction
# # X0       =  390.255 # [pixel] X-coordinate of principle
# # Y0       =  242.329 # [pixel] Y-coordinate of principle
# # 
# # [EXTERNAL]
# # B        =  0.20    # [m] width of baseline of stereo camera rig
# # X        = -0.83    # [m] distance of rectified images (virtual camera)
# # Y        =  0.00    # [m] lateral position of rectified images (virtual camera)
# # Z        =  1.28    # [m] height of rectified images (virtual camera)
# # TILT     =  0.0062  # [rad] tilt angle
# # YAW      =  0.0064  # [rad] yaw angle
# # ROLL     =  0.0009  # [rad] roll angle
# # 
# # # Notes:
# # #  In a stereo camera system the internal parameters for both cameras are the
# # #  same.
# # #
# # #  The camera position (X, Y, Z) is given in car coordinates.
# # #  For the definition of the camera and car coordinate system and the rotation 
# # #  angles see the image carcameracoord.png.

f        =  985.939 # [pixel] focal length
u0       =  390.255 # [pixel] X-coordinate of principle
v0       =  242.329 # [pixel] Y-coordinate of principle
b        =  0.20    # [m] width of baseline of stereo camera rig


# need a function to refine a point feature match
#   PointFeature.refinematch(pf1, pf2, im2)
#      pull 3 windows from im2 using coordinate in pf2
#      compute the distances
#      fit parabola and solve it

clear T
randinit
## matching
for i=1:10
    i
    L = left(:,:,i)
    R = right(:,:,i)
# compute corners

    cl = isift(L, 'nfeat', 200)
    cr = isift(R, 'nfeat', 200)
    
    ms = cl.match(cr)
    
    F = ms.ransac(@fmatrix, 1e-4)
    
    figure[0]
    idisp({L,R})
    ms.inlier.plot('w')
    
    cam = CentralCamera('image', left(:,:,1))
    #cam.plot_epiline(F', m.inlier.subset[29].p2, 'r')
    
    p = ms.inlier.p
    
    p1 = p(1:2,:) p2 = p(3:4,:)

    d = p1(1,:) - p2(1,:)
    X = b * (p1(1,:) - u0) ./ d
    Y = b * (p1(2,:) - v0) ./ d
    Z = f * b ./ d
    P = [X Y; Z]
    
    figure[1]
    plot3(X, Y, Z, 'o')
    xyzlabel
    grid on
    
    cl = cl([ms.inlier_]) # keep just the inliers
    
    if i > 1
        # match all the inliers for which we have 3D points with old corners
        [mt,Ct] = cl.match(clp)
        Ft = mt.ransac(@fmatrix, 1e-4)
        
        figure[3]
            ms.inlier.plot('y')

            
        mt.show
        
        p = mt.inlier.p
    
        figure[1]
    hold on
        plot3(X, Y, Z, '*')
        hold off
        
        k = [mt.inlier_]
        j = Ct(1,k)
        jp = Ct(2,k)
        
        TT = icp(Pp(:,jp), P(:,j), 'distthresh', 5, 'maxtheta', 0.05, 'verbose')
        T(i) = SE3(TT)
    end
    Pp = P
    clp =     cl # just keep the inliers
    crp = cr([ms.inlier_])
    Lp = L

    
    
    pause(0.5)
end
