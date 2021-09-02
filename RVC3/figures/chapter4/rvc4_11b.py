#!/usr/bin/env python3

import bdsim
import math

bd = bdsim.BlockDiagram()

# parameters
xg = [5, 5, math.pi/2]
Krho = bd.GAIN(1)
Kalpha = bd.GAIN(5)
Kbeta = bd.GAIN(-2)
xg = [5, 5, math.pi/2]
x0 = [5, 2, 0]

# annotate the graphics
def graphics(ax):
    ax.plot(*xg[0:2], '*')
    ax.plot(*x0[0:2], 'o')

# convert x,y,theta state to polar form
def polar(x, dict):
    rho = math.sqrt(x[0]**2 + x[1]**2)

    if not 'direction' in dict:
        # direction not yet set, set it
        beta = -math.atan2(-x[1], -x[0])
        alpha = -x[2] - beta
        dict['direction'] = -1 if -math.pi/2 <= alpha < math.pi/2 else 1
        print('set direction to ', dict['direction'])

    
    if dict['direction'] == -1:
        beta = -math.atan2(x[1], x[0]);
    else:
        beta = -math.atan2(-x[1], -x[0])
    alpha = -x[2] - beta

    # clip alpha
    if alpha > math.pi/2:
        alpha = math.pi/2
    elif alpha < -math.pi/2:
        alpha = -math.pi/2  

    return [rho, alpha, beta, dict['direction']]

# constants
goal0 = bd.CONSTANT([xg[0], xg[1], 0])
goalh = bd.CONSTANT(xg[2])

# stateful blocks
bike = bd.BICYCLE(x0=x0, name='bike')

# functions
polar = bd.FUNCTION(polar, nout=4, dict=True, name='polar', inp_names=('x',),
    outp_names=(r'$\rho$', r'$\alpha$', r'$\beta', 'direction'))
stop = bd.STOP(lambda x: x < 0.01, name='close enough')
steer_rate = bd.FUNCTION(lambda u: math.atan(u), name='atan')

# arithmetic
vprod = bd.PROD('**', name='vprod')
aprod = bd.PROD('**/', name='aprod')
xerror = bd.SUM('+-')
heading_sum = bd.SUM('++', angles=True)
gsum = bd.SUM('++')

# displays
xyscope = bd.VEHICLEPLOT(scale=[0, 10], size=0.7, shape='box', init=graphics)
ascope = bd.SCOPE(name=r'$\alpha$')
bscope = bd.SCOPE(name=r'$\beta$')

# connections

mux = bd.MUX(3)

bd.connect(bike[0:3], mux[0:3], xyscope[0:3])
bd.connect(mux, xerror[0])
bd.connect(goal0, xerror[1])

bd.connect(xerror, polar)
bd.connect(polar[0], Krho, stop) # rho
#bd.connect(Krho, vprod[1])
vprod[1] =  polar[0] * bd.GAIN(1)
vprod[0] = polar[4]

bd.connect(polar[1], Kalpha, ascope) # alpha
bd.connect(Kalpha, gsum[0])
bd.connect(polar[2], heading_sum[0]) # beta
bd.connect(goalh, heading_sum[1])
#bd.connect(heading_sum, Kbeta, bscope)
heading_sum[0] = polar.alpha *bd.GAIN(5, 'Kalpha')
heading_sum[1] = polar.beta * bd.GAIN(-2, 'Kbeta')
aprod[0] = heading_sum
aprod[1] = polar.direction
#bd.connect(polar[3], vprod[0], aprod[1])


#bd.connect(vprod, fabs, bike.v)
bike.v = vprod
bike.gamma = aprod * bd.FUNCTION(lambda x: abs(x), name='abs')

bd.connect(aprod, steer_rate)
bd.connect(steer_rate, bike.gamma)

bd.connect(Kbeta, gsum[1])
bd.connect(gsum, aprod[0])

bd.compile()
bd.report()
bd.dotfile('rvc4_11.dot')

out = bd.run(block=True)

bd.done()
