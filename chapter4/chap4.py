## Matlab commands extracted from /Users/corkep/doc/svn/book/src/mobile/chap.tex

from math import pi
import roboticstoolbox as rtb

## 4.1.1

# sl_lanechange

# sim('sl_lanechange')

# out

# t = out.get('t') q = out.get('y')

# mplot(t, q)

# plot(q[:,0], q[:,1])

# ## 4.1.1.1


# sl_drivepoint

# xg = [5, 5]

# x0 = [8, 5, pi / 2]

# r = sim('sl_drivepoint')

# q = r.find('y')

# plot(q[:,0], q[:,1])

# ## 4.1.1.2

# sl_driveline

# L = [1, -2, 4]

# x0 = [8, 5, pi / 2]

# r = sim('sl_driveline')

# ## 4.1.1.3

# sl_pursuit

# r = sim('sl_pursuit')


# ## 4.1.1.4 move to pose

# sl_drivepose

# xg = [5, 5, pi / 2]

# x0 = [9, 5, 0]

# r = sim('sl_drivepose')

# q = r.find('y')
# plot(q[:,0], q[:,1])

# ## 4.1.2 diff steer

# ## 4.2 flying robots

# sl_quadrotor

# mdl_quadrotor

# sim('sl_quadrotor')


# about result

# plot(result(:,1), result(:,2:3))

veh = rtb.Bicycle(speed_max=1, steer_max=30 * pi / 180)
print(veh)
d = veh.deriv([], [0, 0, 0], [0.3, 0.2])
print(d)
