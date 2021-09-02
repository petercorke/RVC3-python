from rvcprint import rvcprint
from fig9_18 import PumaCollapse
import matplotlib.pyplot as plt
import roboticstoolbox as rtb

out = PumaCollapse()

plt.figure()
rtb.qplot(out.t, out.x[:,:3])
rtb.ylabel('q (rad)')
# plt.grid(True)
# plt.xlabel('Time (s)')
rvcprint()