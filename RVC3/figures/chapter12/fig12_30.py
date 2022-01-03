#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

# generate PDFs to be included in the ezdraw figure
mona = Image.Read('monalisa.png', grey=True, dtype='float')
G, L, s = mona.scalespace(8, 8)
for i in range(4):
    h = G[i].disp(plain=True)
    plt.gcf().savefig(f"G{i:d}.pdf")
for i in range(3):
    h = L[i].disp(plain=True, colormap="signed")
    plt.gcf().savefig(f"L{i:d}.pdf")

