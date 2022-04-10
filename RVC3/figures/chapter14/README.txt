==================== GENERAL ====================
This directory contains eucsbademo, an example of using sba for Euclidean bundle adjustment.
Refer to ICS/FORTH TR-340 for documentation on sba. eucsbademo implements two variants of
Euclidean BA: a) BA for camera poses and scene structure assuming intrinsics are fixed and
identical for all cameras, b) BA for camera intrinsics, poses and scene structure assuming
intrinsics vary among cameras and c) BA for camera intrinsics, distortion, poses and scene
structure assuming intrinsics & distortion vary among cameras.

** For a), eucsbademo accepts 3 file names as arguments:
They are the initial estimates for the camera motion (i.e. pose) parameters, the initial
estimates for the 3D point parameters along with the 3D points image projections and the
camera intrinsic calibration parameters. The file for the camera motion parameters has a
separate line for every camera (i.e. frame), each line containing 7 parameters (a 4
element quaternion for rotation and a 3 element vector for translation). Rotation
quaternions have the scalar part as their first element, i.e. a rotation by angle TH
around the unit vector U=(Ux, Uy, Uz) should be specified as
cos(TH/2) Ux*sin(TH/2) Uy*sin(TH/2) Uz*sin(TH/2).
The file for 3D points and image projections is made up of lines of the form 

X Y Z  NFRAMES  FRAME0 x0 y0  FRAME1 x1 y1 ...

each corresponding to a single 3D point. X Y Z are the points' Euclidean 3D coordinates,
NFRAMES the total number of images in which the points' projections are available and each
of the NFRAMES subsequent triplets FRAME x y specifies that the 3D point in question projects
to pixel x y in image FRAME. For example, the line

100.0 200.0 300.0 3  2 270.0 114.1 4 234.2 321.7 5 173.6 425.8

specifies the 3D point (100.0, 200.0, 300.0) projecting to the 3 points (270.0, 114.1),
(234.2, 321.7) and (173.6, 425.8) in images 2, 4 and 5 respectively. Pixel coordinates
are measured using the common convention, i.e. from the top left corner of images with
the positive x axis running from left to right and y from top to bottom. Camera and 3D
point indices count from 0.

** For b), eucsbademo accepts 2 file names as arguments, specifically the file defining the
inital estimates for the camera intrinsics and motion parameters and that defining the initial
estimates for the 3D point parameters along with the 3D points image projections.
The file for the camera parameters has a separate line for every camera, each line
containing 12 parameters (the five intrinsic parameters in the order focal length in x pixels,
principal point coordinates in pixels, aspect ratio [i.e. focalY/focalX] and skew factor,
plus a 4 element quaternion for rotation and a 3 element vector for translation).
The format of the file for 3D points and image projections is identical to that explained
for case a) above. The number of intrincic parameters to be kept fixed can also be selected
(e.g., fixed skew, fixed aspect ratio and skew, fixed aspect ratio, skew and principal point),
check the first few lines of sba_driver().

** For c), eucsbademo accepts 2 file names as arguments, specifically the file defining the
inital estimates for the camera intrinsics, distortions and motion parameters and that defining
the initial estimates for the 3D point parameters along with the 3D points image projections.
The file for the camera parameters has a separate line for every camera, each line
containing 17 parameters (the five intrinsic parameters in the order focal length in x pixels,
principal point coordinates in pixels, aspect ratio [i.e. focalY/focalX] and skew factor,
the five distortion parameters vector kc (more below) plus a 4 element quaternion for rotation
and a 3 element vector for translation).
The format of the file for 3D points and image projections is identical to that explained
for case a) above. The number of intrincic parameters to be kept fixed can also be selected
(e.g., fixed skew, fixed aspect ratio and skew, fixed aspect ratio, skew and principal point),
check the first few lines of sba_driver().
Similarly, the number of distortion parameters to be kept fixed can be selected
(e.g. fixed 6th/4th/2nd order radial distortion, fixed tangential distortion).

The employed distortion model is the one used by Bouguet, see
http://www.vision.caltech.edu/bouguetj/calib_doc/htmls/parameters.html.

According to this model, radial and tangential distortion is specified
by a five-vector kc with the following elements:

kc[0] is the 2nd order radial distortion coefficient
kc[1] is the 4th order radial distortion coefficient
kc[2], kc[3] are the tangential distortion coefficients
kc[4] is the 6th order radial distortion coefficient

More specifically, assume x_n=(x, y)=(X/Z, Y/Z) is the pinhole image projection
and let r^2=x^2+y^2. The distorted image projection is defined as

x_d=(1 + kc[0]*r^2 + kc[1]*r^4 + kc[4]*r^6)*x_n + dx,
with
dx=(2*kc[2]*x*y + kc[3]*(r^2+2*x^2), kc[2]*(r^2+2*y^2) + 2*kc[3]*x*y).
The distorted point in pixel coordinates is given by K*x_d, K being the intrinsics.

Note that zero-based indexing is used above, Bouguet's page conforms to
Matlab's convention and uses one-based indexing!

======================= POINT COVARIANCES =======================
Starting in ver. 1.5, sba supports the incorporation into BA of covariance information
for image points. To accept such covariances, eucsbademo extends the points file format
defined above to lines of the form

X Y Z  NFRAMES  FRAME0 x0 y0 covx0^2 covx0y0 covx0y0 covy0^2  FRAME1 x1 y1 covx1^2 covx1y1 covx1y1 covy1^2 ...

In other words, the covariance matrices simply follow the corresponding image coordinates.
It is also possible to slightly reduce the file size by specifying only the upper
triangular part of covariance matrices, e.g. covx0^2 covx0y0 covy0^2, etc

==================== ROTATION PARAMETRIZATION ====================
In all a), b) and c) cases above, the eucsbademo program describes rotations using a
local rotation representation: Given an initial rotation estimate R0, a refined rotation
R can be factorized as R=Rs*R0, where Rs is a small rotation to be estimated. An initial
estimate corresponding to zero rotation is used for Rs, i.e. a quaternion equal to
(1, 0, 0, 0). The eucsbademo program parametrizes Rs internally using only the vector
part of the corresponding quaternion, i.e. 3 parameters per camera: Assuming positive
scalar components w, the former can be determined uniquely from the vector parts (x, y, z)
as w=sqrt(1-x^2-y^2-z^2).

==================== FILES ====================
eucsbademo.c:  main demo program
readparams.c:  functions to read the initial motion and structure estimates from text files
imgproj.c:     functions to estimate the projection on a given camera of a certain 3D point. Also
               includes code for evaluating the corresponding jacobian
eucsbademo.h:  function prototypes
readparams.h:  function prototypes

calib.txt:     intrinsic calibration matrix K for the employed camera (used only in the fixed K test cases)

7cams.txt:     initial motion parameters for a test case involving 7 cameras (fixed K)
7camsvarK.txt: initial intrinsic & motion parameters for the 7 cameras test case (varying K)
7pts.txt:      initial structure parameters for the 7 cameras test case

9cams.txt:     initial motion parameters for a test case involving 9 cameras (fixed K)
9camsvarK.txt: initial intrinsic & motion parameters for the 9 cameras test case (varying K)
9pts.txt:      initial structure parameters for the 9 cameras test case

54cams.txt:      initial motion parameters for a test case involving 54 cameras (fixed K)
54camsvarK.txt:  initial intrinsic & motion parameters for the 54 cameras test case (varying K)
54camsvarKD.txt: initial intrinsic, distortion & motion parameters for the 54 cameras test case (varying K & distortion kc)
54pts.txt:       initial structure parameters for the 54 cameras test case

==================== COMPILING ====================
The demo program is built during sba's compilation

==================== SAMPLE RUNS ====================
The command
  eucsbademo 7cams.txt 7pts.txt calib.txt
produces the following output:

  Starting BA with fixed intrinsic parameters
  SBA using 465 3D pts, 7 frames and 1916 image projections, 1437 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, fixed intrinsics

  SBA returned 17 in 17 iter, reason 2, error 0.675396 [initial 19.0947], 18/17 func/fjac evals, 24 lin. systems
  Elapsed time: 0.34 seconds, 340.00 msecs
whereas command
  eucsbademo 7camsvarK.txt 7pts.txt
produces the following output:
  Starting BA with varying intrinsic parameters
  SBA using 465 3D pts, 7 frames and 1916 image projections, 1472 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, variable intrinsics (2 fixed)

  SBA returned 150 in 150 iter, reason 3, error 0.659201 [initial 19.0947], 153/150 func/fjac evals, 170 lin. systems
  Elapsed time: 5.29 seconds, 5290.00 msecs


For the 9 cameras case,
  eucsbademo 9cams.txt 9pts.txt calib.txt
produces
  Starting BA with fixed intrinsic parameters
  SBA using 559 3D pts, 9 frames and 2422 image projections, 1731 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, fixed intrinsics

  SBA returned 17 in 17 iter, reason 2, error 0.619559 [initial 8.17604], 18/17 func/fjac evals, 25 lin. systems
  Elapsed time: 0.45 seconds, 450.00 msecs
and
  eucsbademo 9camsvarK.txt 9pts.txt
produces
  Starting BA with varying intrinsic parameters
  SBA using 559 3D pts, 9 frames and 2422 image projections, 1776 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, variable intrinsics (2 fixed)

  SBA returned 150 in 150 iter, reason 3, error 0.600039 [initial 8.17603], 154/150 func/fjac evals, 180 lin. systems
  Elapsed time: 6.90 seconds, 6900.00 msecs


For the 54 cameras case,
  eucsbademo 54cams.txt 54pts.txt calib.txt
produces
  Starting BA with fixed intrinsic parameters
  SBA using 5207 3D pts, 54 frames and 24609 image projections, 15945 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, fixed intrinsics

  SBA returned 21 in 21 iter, reason 2, error 0.176473 [initial 2.14707], 22/21 func/fjac evals, 29 lin. systems
  Elapsed time: 7.99 seconds, 7990.00 msecs
typing
  eucsbademo 54camsvarK.txt 54pts.txt
produces
  Starting BA with varying intrinsic parameters
  SBA using 5207 3D pts, 54 frames and 24609 image projections, 16215 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, without distortion, variable intrinsics (2 fixed)

  SBA returned 36 in 36 iter, reason 2, error 0.134928 [initial 2.14707], 36/36 func/fjac evals, 47 lin. systems
  Elapsed time: 28.58 seconds, 28580.00 msecs
and
  eucsbademo 54camsvarKD.txt 54pts.txt
produces
  Starting BA with varying intrinsic parameters & distortion
  SBA using 5207 3D pts, 54 frames and 24609 image projections, 16485 variables

  Method BA_MOTSTRUCT, expert driver, analytic Jacobian, without covariances, variable distortion (3 fixed), variable intrinsics (2 fixed)

  SBA returned 34 in 34 iter, reason 2, error 0.128779 [initial 2.14707], 34/34 func/fjac evals, 44 lin. systems
  Elapsed time: 55.17 seconds, 55170.00 msecs


Send your comments/questions to lourakis@ics.forth.gr
