from pathlib import Path
from machinevisiontoolbox import *
from roboticstoolbox import *

from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt
from math import pi, sqrt, atan2


sim = BDSim(animation=True) #debug='i')
bd = sim.blockdiagram()

clock = bd.clock(0.1, unit='s')

# wide angle camera
camera = CentralCamera.Default(f=0.002)
T_vc = SE3(0.2, 0.1, 0.3) * SE3.Ry(pi/2) * SE3.Rz(-pi/2) #*trotx(-pi/4);   
P = np.array([[4.0, 10, 3], [9, 9, 2], [6, 8, 3], [8, 10, 4], [10, 7, 2]]).T
T_B_C = SE3(0.2, 0.1, 0.5) * SE3.Ry(pi/2) * SE3.Rz(-pi/2)
x0 = [2, 2, 0];
# xg = [5 5 pi/2];

# convert x,y,theta state to polar form
def polar(x, dict):
    rho = sqrt(x[0]**2 + x[1]**2)

    if not 'direction' in dict:
        # direction not yet set, set it
        beta = -atan2(-x[1], -x[0])
        alpha = -x[2] - beta
        print('alpha', alpha)
        if -pi / 2 <= alpha <= pi / 2:
            dict['direction'] = 1
        else:
            dict['direction'] = -1
        print('set direction to ', dict['direction'])

    if dict['direction'] == -1:
        beta = -atan2(x[1], x[0]);
    else:
        beta = -atan2(-x[1], -x[0])
    alpha = -x[2] - beta

    # clip alpha
    if alpha > pi/2:
        alpha = pi/2
    elif alpha < -pi/2:
        alpha = -pi/2  

    return [dict['direction'], rho, alpha, beta, ]

model = Path(__file__).parent / "IBVS-nonholonomic.bd"
print(model)


def world_init(ax):
	# plot X, Y coords of world points
	ax.plot(P[0, :], P[1, :], 'b*')


bd = bdload(bd, model, globalvars=globals())
bd.report()
bd.compile()
bd.report()

print('about to run')
print(sim.options)
sim.set_options(animation=False)
out = sim.run(bd, 30)
print('done')
print(out)

# sim.done(bd)
# plt.pause(5)
