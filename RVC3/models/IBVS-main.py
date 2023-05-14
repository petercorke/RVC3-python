from pathlib import Path
from machinevisiontoolbox import *
from bdsim import Clock, bdload, BDSim
from spatialmath import SE3
import matplotlib.pyplot as plt


sim = BDSim(animation=True) #debug='i')
bd = sim.blockdiagram()

clock = bd.clock(0.1, unit='s')
camera = CentralCamera.Default()

lmbda = 0.1
pose_0 = SE3(1, 1, -3) * SE3.Rz(0.6)

model = Path(__file__).parent / "IBVS.bd"
print(model)

def plot_init(camera):
	print('@@@@@plot_init')
	camera.plot_point(bd['p*'].value, 'b*')


bd = bdload(bd, model, globalvars=globals())
bd.compile()

sim.report(bd)
out = sim.run(bd, 50)

