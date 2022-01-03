#!/usr/bin/env python3
import rvcprint
from machinevisiontoolbox import Image

flowers = Image.Read('flowers8.png')

flowers.plane(0).colorize((1, 0, 0)).disp()
rvcprint.rvcprint(subfig='a')

flowers.plane(1).colorize((0, 1, 0)).disp()
rvcprint.rvcprint(subfig='b')

flowers.plane(2).colorize((0, 0, 1)).disp()
rvcprint.rvcprint(subfig='c')
