#!/usr/bin/env python3

import rvcprint
import numpy as np
import matplotlib.pyplot as plt
from machinevisiontoolbox import *
from matplotlib.ticker import ScalarFormatter
from matplotlib import cm

    system( sprintf('ps2eps -l #s.pdf', fname) )
    system( sprintf('epstopdf #s.eps', fname) )
    system( sprintf('pdf2ps  #s.pdf', fname) )
    system( sprintf('rm -f #s.eps', fname) )
    system( sprintf('ps2eps -l #s.ps', fname) )
    system( sprintf('mv #s.eps newfigs', fname) )
    system( sprintf('rm -f #s.pdf #s.ps', fname, fname) )
