#!/usr/bin/env python3

# from RVC3.tools import rvcprint
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

# from RVC3.tools import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
import spatialmath.base as smb

# load .enpeda dataset, 12bit pixel values
args = dict(mono=True, dtype="uint8", maxintval=4095, roi=[20, 750, 20, 480])
try:
    lefts = ZipArchive("bridge-l.zip", filter="*.pgm", **args)
    rights = ZipArchive("bridge-r.zip", filter="*.pgm", **args)
except ValueError:
    print(
        "you will need to download the .enpeda bridge dataset, see the instructions at https://ssdfsfsd"
    )

# camera intrinsics
f = 985.939  # [pixel] focal length
u0 = 390.255  # [pixel] X-coordinate of principle
v0 = 242.329  # [pixel] Y-coordinate of principle
b = 0.20  # [m] width of baseline of stereo camera rig

cam = CentralCamera(f=f, pp=[u0, v0], rho=[1, 1])
print(cam)

cv.setRNGSeed(0)

displacements = []
errors = []
nmatches = []

nframes = 0
n_lr_fail = 0
n_fb_fail = 0
n_no_overlap = 0
n_optimized = 0

for left, right in zip(lefts, rights):
    nframes += 1
    print("-----------------", left.id)
    # plt.clf()
    # plt.imshow(image.A, cmap='gray')
    # smb.plot_text((20, 420), f"frame {image.id}", color='w', backgroundcolor='k', fontsize=12)

    # find corner features
    orbL = left.ORB(nfeatures=400, id="index")
    orbR = right.ORB(nfeatures=400)

    # robustly match left and right corner features
    # - stereo match
    matchLR = orbL.match(orbR)
    try:
        F = matchLR.estimate(cam.points2F, method="ransac")
    except ValueError as e:
        # too few/degenerate stereo correspondences to triangulate this
        # frame at all -- skip it entirely, keep the last good frame as
        # the temporal reference for the next one
        print(f"  stereo F estimation failed for frame {left.id}: {e}")
        n_lr_fail += 1
        continue
    print(matchLR)

    matchLR = matchLR.inliers  # just keep the inliers
    nmatches.append(len(matchLR))

    # triangulate 3D points
    # m2 = m[::100]  # short list of matches
    lines1 = cam.ray(matchLR.p1)
    T = SE3(b, 0, 0)
    lines2 = cam.move(T).ray(matchLR.p2)

    P, d = lines1.closest_to_line(lines2)
    print(np.nanmedian(d))

    if left.id > 0:
        # if we have a previous frame

        # display two sequential stereo pairs
        plt.clf()
        view4 = Image.Tile([left, right, left_prev, right_prev], columns=2, sep=0)
        plt.imshow(view4.A, cmap="gray")

        matchLR.plot_correspondence("y", offset=(left.width, 0), linewidth=0.5)

        # temporal matching
        matchFB = orbL.match(orbL_prev)
        try:
            F = matchFB.estimate(cam.points2F, method="ransac")
            print(matchFB)
            matchFB = matchFB.inliers  # keep the inliers
            matchFB.plot_correspondence("y", offset=(0, left.height), linewidth=0.5)
            plt.pause(0.1)
        except ValueError as e:
            # too few/degenerate temporal correspondences -- same downstream
            # effect as zero overlapping landmarks below (no valid frame
            # motion estimate), but caught earlier since points2F() itself
            # can't even find a fundamental matrix here
            print(f"  temporal F estimation failed for frame {left.id}: {e}")
            n_fb_fail += 1
            matchFB = None

        # if left.id == 10:
        #     rvcprint.rvcprint(thicken=None)

        # now create a bundle adjustment problem, if we have a usable
        # temporal match -- skip frames where no ORB feature was matched
        # both stereo (left/right) and temporally (this frame/previous
        # frame), since optimize() has nothing to refine in that case.
        # Append NaN placeholders rather than nothing, so
        # displacements/errors stay frame-aligned with nmatches.
        landmarks_added = False
        if matchFB is not None:
            ba = BundleAdjust(cam)

            c_left = ba.add_view(
                SE3(), fixed=True
            )  # first camera at origin (current frame)
            c_leftprev = ba.add_view(
                SE3()
            )  # initial guess, zero motion (prev frame)

            for k, Pk in enumerate(P.T):  # for every 3D point from stereo
                if np.any(np.isnan(Pk)):
                    continue  # discard bad matches

                id = matchLR[k].id1
                m = matchFB.by_id1(id)
                if m is None:
                    continue
                landmark = ba.add_landmark(Pk)
                ba.add_projection(c_left, landmark, m.p1)  # current left camera
                ba.add_projection(
                    c_leftprev, landmark, m.p2
                )  # previous left camera
                landmarks_added = True

        if landmarks_added:
            X, error = ba.optimize(iterations=5)
            displacements.append(X[6:12])
            errors.append(error)
            n_optimized += 1
        else:
            print(
                f"  no overlapping stereo/temporal landmarks for frame "
                f"{left.id} -- skipping bundle adjustment"
            )
            n_no_overlap += 1
            displacements.append(np.full(6, np.nan))
            errors.append(np.nan)

    # keep images and features for next cycle
    orbL_prev = orbL
    left_prev = left
    right_prev = right

print()
print("===== summary =====")
print(f"frames processed:            {nframes}")
print(f"stereo (LR) F estimation failed:   {n_lr_fail}")
print(f"temporal (FB) F estimation failed: {n_fb_fail}")
print(f"no overlapping LR/FB landmarks:    {n_no_overlap}")
print(f"bundle adjustment ran:             {n_optimized}")

# since it took so long to compute, let's save the results
with open("vo.pickle", "wb") as f:
    d = dict(displacements=displacements, errors=errors, nmatches=nmatches)
    pickle.dump(d, f)
