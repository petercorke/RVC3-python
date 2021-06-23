#!/usr/bin/env python3

# run with command line -a switch to show animation

import bdsim
import numpy as np
import math
import roboticstoolbox as rtb
import bdsim

# parameters for the path
look_ahead = 5
speed = 1
dt = 0.1
tacc = 1

# create the path
path = np.array([
    [10, 10],
    [10, 60],
    [80, 80],
    [50, 10]
    ])
      
robot_traj = rtb.mstraj(path[1:,:], qdmax=speed, q0=path[0,:], dt=0.1, tacc=tacc).q
total_time = robot_traj.shape[0] * dt + look_ahead / speed

sim = bdsim.BDSim(graphics=False)
bd = sim.blockdiagram()

def background_graphics(ax):
    ax.plot(path[:,0], path[:,1], 'r', linewidth=3, alpha=0.7)

def pure_pursuit(cp, R=None, traj=None):
    # find closest point on the path to current point
    d = np.linalg.norm(traj-cp, axis=1) # rely on implicit expansion
    i = np.argmin(d)
    
    # find all points on the path at least R away
    k, = np.where(d[i+1:] >= R)  # find all points beyond horizon
    if len(k) == 0:
        # no such points, we must be near the end, goal is the end
        pstar = traj[-1,:]
    else:
        # many such points, take the first one
        k = k[0]  # first point beyond look ahead distance
        pstar = traj[k+i,:]
    return pstar.flatten()


speed = bd.CONSTANT(speed, name='speed')
error = bd.SUM('+-', name='err')
#d2goal = bd.FUNCTION(lambda d: math.sqrt(d[0]**2 + d[1]**2), name='d2goal')
h2goal = bd.FUNCTION(lambda d: math.atan2(d[1], d[0]), name='h2goal')
heading_error = bd.SUM('+-', angles=True, name='herr')
Kh = bd.GAIN(0.5, name='Kh')
bike = bd.BICYCLE(x0=[2, 2, 0])
vplot = bd.VEHICLEPLOT(scale=[0, 80, 0, 80], size=0.7, shape='box', init=background_graphics) #, movie='rvc4_8.mp4')
sscope = bd.SCOPE(name='steer angle')
hscope = bd.SCOPE(name='heading angle')
mux = bd.MUX(2)
stop = bd.STOP(lambda x: np.linalg.norm(x - np.r_[50,10]) < 0.1, name='close_enough')
pp = bd.FUNCTION(pure_pursuit, kwargs={'R': look_ahead, 'traj': robot_traj}, name='pure_pursuit')

bd.connect(pp, error[0])
bd.connect(error, h2goal)
#bd.connect(d2goal, stop)

bd.connect(h2goal, heading_error[0])
bd.connect(bike[2], heading_error[1], hscope)
bd.connect(heading_error, Kh)
bd.connect(Kh, bike[1], sscope)
bd.connect(speed, bike[0])

bd.connect(bike[0:2], mux)
bd.connect(mux, pp, error[1], stop)

bd.connect(bike[0:3], vplot[0:3])

bd.compile()

if __name__ == "__main__":
    bd.report()
    print('\nSimulating for ', total_time, ' seconds')
    out = sim.run(bd, T=total_time)
