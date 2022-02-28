from pathlib import Path
from machinevisiontoolbox import *
from roboticstoolbox import *

from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt
from math import pi


sim = BDSim(animation=True) #debug='i')
bd = sim.blockdiagram()

clock = bd.clock(0.1, unit='s')

# wide angle camera
camera = CentralCamera.Default(f=0.002)
T_vc = SE3(0.2, 0.1, 0.3) * SE3.Ry(pi/2) * SE3.Rz(-pi/2) #*trotx(-pi/4);   
P = np.array([[0, 0], [1, -1], [2, 2]])
pd = camera.project_point(P, pose=SE3(-2, 0, 0)*T_vc)

q0 = [-8, 2, 0.3]
lmbda = 1

model = Path(__file__).parent / "IBVS-holonomic.bd"
print(model)

def plot_init(camera):
	camera.plot_point(pd, 'b*')

def world_init(ax):
	# plot X, Y coords of world points
	ax.plot(P[0, :], P[1, :], 'b*')


bd = bdload(bd, model, globalvars=globals())
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
